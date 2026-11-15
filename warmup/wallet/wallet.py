from dataclasses import dataclass
from decimal import Decimal
from wallet.errors import InsufficientFundsError
from wallet.money import SUPPORTED_CURRENCIES, to_positive_money, validate_currency

@dataclass(frozen=True)
class Transaction:
    kind: str
    currency: str
    amount: Decimal
    balance_after: Decimal

class Wallet:

    def __init__(self, owner: str) -> None:
        self.owner = owner
        self._balances: dict[str, Decimal] = {c: Decimal('0.00') for c in SUPPORTED_CURRENCIES}
        self._history: list[Transaction] = []

    def balance(self, currency: str) -> Decimal:
        validate_currency(currency)
        return self._balances[currency]

    def deposit(self, currency: str, amount, kind: str='deposit') -> Decimal:
        validate_currency(currency)
        value = to_positive_money(amount)
        self._balances[currency] += value
        self._record(kind, currency, value)
        return self._balances[currency]

    def withdraw(self, currency: str, amount, kind: str='withdrawal') -> Decimal:
        validate_currency(currency)
        value = to_positive_money(amount)
        if value > self._balances[currency]:
            raise InsufficientFundsError(f'{self.owner} has {self._balances[currency]} {currency}, needs {value}')
        self._balances[currency] -= value
        self._record(kind, currency, value)
        return self._balances[currency]

    def history(self, currency: str | None=None, kind: str | None=None) -> list[Transaction]:
        if currency is not None:
            validate_currency(currency)
        return [t for t in self._history if (currency is None or t.currency == currency) and (kind is None or t.kind == kind)]

    def _record(self, kind: str, currency: str, amount: Decimal) -> None:
        self._history.append(Transaction(kind, currency, amount, self._balances[currency]))
