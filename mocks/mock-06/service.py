"""Business logic for merchants and payments. In-memory only.

Takes plain arguments (not Pydantic models) so it can be reused by any caller:
the HTTP routes today, bulk or CSV import later.
"""

import uuid
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation

from errors import (
    IdempotencyConflict,
    InvalidPayment,
    InvalidTransition,
    PaymentNotFound,
    RefundExceedsCaptured,
    UnknownMerchant,
)
from models import Merchant, PaymentOut, PaymentStatus

SUPPORTED_CURRENCIES = frozenset({"USD", "EUR", "GBP"})

# Allowed status changes. Anything not listed is an InvalidTransition.
# FAILED and REFUNDED are terminal.
TRANSITIONS: dict[PaymentStatus, frozenset[PaymentStatus]] = {
    PaymentStatus.PENDING: frozenset({PaymentStatus.CAPTURED, PaymentStatus.FAILED}),
    PaymentStatus.CAPTURED: frozenset(
        {PaymentStatus.PARTIALLY_REFUNDED, PaymentStatus.REFUNDED}
    ),
    PaymentStatus.PARTIALLY_REFUNDED: frozenset(
        {PaymentStatus.PARTIALLY_REFUNDED, PaymentStatus.REFUNDED}
    ),
    PaymentStatus.FAILED: frozenset(),
    PaymentStatus.REFUNDED: frozenset(),
}

# Statuses a refund may start from. PENDING / FAILED / REFUNDED are rejected.
REFUNDABLE_STATUSES = frozenset({PaymentStatus.CAPTURED, PaymentStatus.PARTIALLY_REFUNDED})

# The exact request body, used for idempotency comparison:
# (merchant_id, amount as sent, currency, idempotency_key)
RequestBody = tuple[str, str | int | Decimal, str, str]


class PaymentsService:
    def __init__(self) -> None:
        # merchant_id -> Merchant
        self._merchants: dict[str, Merchant] = {}
        # payment_id -> PaymentOut
        self._payments: dict[str, PaymentOut] = {}
        # (merchant_id, idempotency_key) -> (exact request body, payment_id)
        self._idempotency: dict[tuple[str, str], tuple[RequestBody, str]] = {}
        # payment_id -> total refunded so far (absent means 0)
        self._refunded: dict[str, Decimal] = {}

    def register_merchant(self, name: str) -> Merchant:
        """Create a merchant with a generated id. No API endpoint; called directly."""
        merchant = Merchant(id=str(uuid.uuid4()), name=name)
        self._merchants[merchant.id] = merchant
        return merchant

    def create_payment(
        self,
        merchant_id: str,
        amount: str | int | Decimal,
        currency: str,
        idempotency_key: str,
    ) -> PaymentOut:
        """Create a pending payment.

        Order of checks:
          1. amount / currency rules  -> InvalidPayment (422)
          2. unknown merchant         -> UnknownMerchant (404)
          3. key seen, same body      -> return the original payment
          4. key seen, different body -> IdempotencyConflict (409)
          5. otherwise create, store, and record the idempotency key
        """
        # 1. business rules
        parsed_amount = self._validate_amount(amount)
        self._validate_currency(currency)

        # 2. merchant must be registered
        if merchant_id not in self._merchants:
            raise UnknownMerchant(f"unknown merchant: {merchant_id}")

        # 3 & 4. idempotency, scoped to the merchant
        scope = (merchant_id, idempotency_key)
        body: RequestBody = (merchant_id, amount, currency, idempotency_key)
        existing = self._idempotency.get(scope)
        if existing is not None:
            original_body, payment_id = existing
            # Exact comparison: "10.50" != "10.5", and 10 != "10" (int vs str).
            if original_body == body and type(original_body[1]) is type(amount):
                return self._payments[payment_id]
            raise IdempotencyConflict(
                f"idempotency key {idempotency_key!r} was already used with a different body"
            )

        # 5. create
        payment = PaymentOut(
            id=str(uuid.uuid4()),
            merchant_id=merchant_id,
            amount=str(parsed_amount),
            currency=currency,
            idempotency_key=idempotency_key,
            status=PaymentStatus.PENDING,
            created_at=datetime.now(timezone.utc),
        )
        self._payments[payment.id] = payment
        self._idempotency[scope] = (body, payment.id)
        return payment

    def get_payment(self, payment_id: str) -> PaymentOut:
        """Look up a payment by id, or raise PaymentNotFound (404)."""
        payment = self._payments.get(payment_id)
        if payment is None:
            raise PaymentNotFound(f"payment not found: {payment_id}")
        return payment

    # --- lifecycle --------------------------------------------------------
    # Rule for every method below: do ALL checks first, then write.
    # A failed call must leave _payments and _refunded untouched.

    def capture(self, payment_id: str) -> PaymentOut:
        """PENDING -> CAPTURED. Full amount only.

        Checks:
          1. payment exists                   -> PaymentNotFound (404)
          2. PENDING -> CAPTURED is allowed   -> InvalidTransition (409)
        Writes:
          3. store the payment with status CAPTURED, return it
        """
        payment = self.get_payment(payment_id)
        self._check_transition(payment, PaymentStatus.CAPTURED)
        return self._set_status(payment, PaymentStatus.CAPTURED)

    def fail(self, payment_id: str) -> PaymentOut:
        """PENDING -> FAILED.

        Checks:
          1. payment exists                   -> PaymentNotFound (404)
          2. current -> FAILED is allowed     -> InvalidTransition (409)
        Writes:
          3. store the payment with status FAILED, return it
        """
        payment = self.get_payment(payment_id)
        self._check_transition(payment, PaymentStatus.FAILED)
        return self._set_status(payment, PaymentStatus.FAILED)

    def refund(self, payment_id: str, amount: str | int | Decimal) -> PaymentOut:
        """Refund part or all of a captured payment.

        Checks:
          1. payment exists                                -> PaymentNotFound (404)
          2. amount passes _validate_amount (reuse)        -> InvalidPayment (422)
          3. status is CAPTURED or PARTIALLY_REFUNDED;
             PENDING / FAILED / REFUNDED can't be refunded -> InvalidTransition (409)
          4. new_total = already refunded + amount
             new_total <= captured amount (payment.amount) -> RefundExceedsCaptured (422)
          5. target status = REFUNDED if new_total == captured,
             else PARTIALLY_REFUNDED; check it's allowed   -> InvalidTransition (409)
        Writes (only after every check passes):
          6. _refunded[payment_id] = new_total
          7. store the payment with the target status, return it
        """
        # --- checks (no writes) ---
        payment = self.get_payment(payment_id)                       # 1
        refund_amount = self._validate_amount(amount)                # 2

        if payment.status not in REFUNDABLE_STATUSES:                # 3
            raise InvalidTransition(
                f"cannot refund a payment with status {payment.status.value!r}"
            )

        captured = Decimal(payment.amount)                           # 4
        new_total = self._refunded.get(payment_id, Decimal("0")) + refund_amount
        if new_total > captured:
            raise RefundExceedsCaptured(
                f"refund of {refund_amount} would bring total refunded to {new_total}, "
                f"exceeding captured amount {captured}"
            )

        target = (                                                   # 5
            PaymentStatus.REFUNDED
            if new_total == captured
            else PaymentStatus.PARTIALLY_REFUNDED
        )
        self._check_transition(payment, target)

        # --- writes (every check passed) ---
        self._refunded[payment_id] = new_total                       # 6
        return self._set_status(payment, target)                     # 7

    def get_refunded_total(self, payment_id: str) -> Decimal:
        """Total refunded so far for a payment (Decimal("0") if none).
        Raises PaymentNotFound (404) for an unknown payment."""
        self.get_payment(payment_id)
        return self._refunded.get(payment_id, Decimal("0"))

    # --- lifecycle helpers ------------------------------------------------

    def _check_transition(self, payment: PaymentOut, target: PaymentStatus) -> None:
        """Raise InvalidTransition unless target is in TRANSITIONS[payment.status].
        Check only; never writes."""
        if target not in TRANSITIONS[payment.status]:
            raise InvalidTransition(
                f"cannot move payment from {payment.status.value!r} to {target.value!r}"
            )

    def _set_status(self, payment: PaymentOut, target: PaymentStatus) -> PaymentOut:
        """Write step: replace the stored payment with
        payment.model_copy(update={"status": target}) and return the copy.
        Call only after all checks have passed."""
        updated = payment.model_copy(update={"status": target})
        self._payments[payment.id] = updated
        return updated

    # --- business-rule validation ---------------------------------------

    def _validate_amount(self, amount: str | int | Decimal) -> Decimal:
        """Reject floats and bools; require a positive value with <= 2 decimals.

        Returns the parsed Decimal. Raises InvalidPayment.
        """
        # bool is a subclass of int, so check it explicitly.
        if isinstance(amount, (bool, float)) or not isinstance(amount, (str, int, Decimal)):
            raise InvalidPayment("amount must be a string, int, or Decimal (not float)")

        try:
            value = Decimal(amount)
        except InvalidOperation:
            raise InvalidPayment(f"amount is not a valid number: {amount!r}")

        # Decimal accepts "NaN" and "Infinity"; money can't be either.
        if not value.is_finite():
            raise InvalidPayment("amount must be a finite number")
        if value <= 0:
            raise InvalidPayment("amount must be positive")
        if value.as_tuple().exponent < -2:
            raise InvalidPayment("amount must have at most 2 decimal places")
        return value

    def _validate_currency(self, currency: str) -> None:
        """Require an exact match in SUPPORTED_CURRENCIES. Raises InvalidPayment."""
        if currency not in SUPPORTED_CURRENCIES:
            raise InvalidPayment(
                f"unsupported currency {currency!r}; must be one of {sorted(SUPPORTED_CURRENCIES)}"
            )
