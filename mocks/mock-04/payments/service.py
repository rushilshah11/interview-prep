from __future__ import annotations

import itertools
from decimal import Decimal

from payments.errors import (
    IdempotencyConflict,
    InvalidTransition,
    NotFound,
    RefundTooLarge,
)
from payments.models import TRANSITIONS, Event, PaymentIntent, Status
from payments.money import check_currency, parse_amount


class PaymentService:
    def __init__(self):
        """Set up in-memory stores for intents, the event log, idempotency keys, and an ID counter."""
        self._intents: dict[str, PaymentIntent] = {}
        self._events: list[Event] = []
        self._keys: dict[str, tuple[str, tuple]] = {}
        self._ids = itertools.count(1)

    def get(self, intent_id: str) -> PaymentIntent:
        """Look up a payment intent by ID, raising NotFound if it does not exist."""
        try:
            return self._intents[intent_id]
        except KeyError:
            raise NotFound(intent_id)

    def events(self, intent_id: str) -> list[Event]:
        """Return the logged status-change events for one intent, in order."""
        self.get(intent_id)
        return [e for e in self._events if e.intent_id == intent_id]

    def create(self, merchant_id: str, amount, currency: str, idempotency_key: str | None = None) -> PaymentIntent:
        """Validate and create a new payment intent, returning the existing one if the idempotency key was already used."""
        value = parse_amount(amount)
        check_currency(currency)
        params = (merchant_id, value, currency)

        if idempotency_key is not None and idempotency_key in self._keys:
            existing_id, _ = self._keys[idempotency_key]
            return self._intents[existing_id]

        intent = PaymentIntent(id=f"pi_{next(self._ids)}", merchant_id=merchant_id, amount=value, currency=currency)
        self._intents[intent.id] = intent
        if idempotency_key is not None:
            self._keys[idempotency_key] = (intent.id, params)
        return intent

    def _move(self, intent: PaymentIntent, to: Status, amount: Decimal | None = None) -> None:
        """Record an event and move the intent to a new status, raising InvalidTransition if the move isn't allowed."""
        if to not in TRANSITIONS[intent.status]:
            raise InvalidTransition(f"{intent.id}: {intent.status.value} -> {to.value}")
        
        self._events.append(Event(intent.id, intent.status, to, amount))
        intent.status = to

    def confirm(self, intent_id: str) -> PaymentIntent:
        """Authorize a created intent."""
        intent = self.get(intent_id)
        self._move(intent, Status.AUTHORIZED)
        return intent

    def capture(self, intent_id: str, amount=None) -> PaymentIntent:
        """Capture the full authorized amount of an intent (partial capture is not implemented yet)."""
        intent = self.get(intent_id)
        if amount is None:
            intent.captured = intent.amount
        else:
            intent.captured = parse_amount(amount)
        self._move(intent, Status.CAPTURED, intent.amount)
        return intent

    def cancel(self, intent_id: str) -> PaymentIntent:
        """Cancel an intent if its current status allows it."""
        intent = self.get(intent_id)
        self._move(intent, Status.CANCELED)
        return intent

    def refund(self, intent_id: str, amount) -> PaymentIntent:
        """Refund part or all of a captured intent, up to its remaining refundable amount."""
        intent = self.get(intent_id)
        if intent.status != Status.CAPTURED:
            raise InvalidTransition(f"{intent.id}: cannot refund while {intent.status.value}")
        value = parse_amount(amount)
        if value > intent.refundable:
            raise RefundTooLarge(f"{intent.id}: {value} > {intent.refundable}")
        intent.refunded += value
        if intent.refundable == 0:
            self._move(intent, Status.REFUNDED, value)
        else:
            self._events.append(Event(intent.id, intent.status, intent.status, value))
        return intent
