"""A wallet holding balances in several currencies, with a transaction history."""

from dataclasses import dataclass
from decimal import Decimal

from wallet.errors import InsufficientFundsError
from wallet.money import SUPPORTED_CURRENCIES, to_positive_money, validate_currency


@dataclass(frozen=True)
class Transaction:
    """One entry in a wallet's history."""

    kind: str  # e.g. "deposit", "withdrawal", "transfer_in", "transfer_out", "fee"
    currency: str
    amount: Decimal
    balance_after: Decimal


class Wallet:
    def __init__(self, owner: str) -> None:
        self.owner = owner
        self._balances: dict[str, Decimal] = {c: Decimal("0.00") for c in SUPPORTED_CURRENCIES}
        self._history: list[Transaction] = []

    def balance(self, currency: str) -> Decimal:
        """Return the current balance for one currency."""
        validate_currency(currency)
        return self._balances[currency]

    def deposit(self, currency: str, amount, kind: str = "deposit") -> Decimal:
        """Add money in one currency and return the new balance."""
        validate_currency(currency)
        value = to_positive_money(amount)
        self._balances[currency] += value
        self._record(kind, currency, value)
        return self._balances[currency]

    def withdraw(self, currency: str, amount, kind: str = "withdrawal") -> Decimal:
        """Remove money in one currency and return the new balance."""
        validate_currency(currency)
        value = to_positive_money(amount)
        if value > self._balances[currency]:
            raise InsufficientFundsError(
                f"{self.owner} has {self._balances[currency]} {currency}, needs {value}"
            )
        self._balances[currency] -= value
        self._record(kind, currency, value)
        return self._balances[currency]

    def history(self, currency: str | None = None, kind: str | None = None) -> list[Transaction]:
        """Return transactions in order, optionally filtered by currency and/or kind."""
        if currency is not None:
            validate_currency(currency)
        return [
            t
            for t in self._history
            if (currency is None or t.currency == currency) and (kind is None or t.kind == kind)
        ]

    def _record(self, kind: str, currency: str, amount: Decimal) -> None:
        self._history.append(Transaction(kind, currency, amount, self._balances[currency]))
