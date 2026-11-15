from __future__ import annotations

from dataclasses import dataclass, field
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation

from ledger.errors import InsufficientFunds, InvalidAmount, UnknownAccount

CENT = Decimal("0.01")


def money(value) -> Decimal:
    if isinstance(value, bool):
        raise InvalidAmount(repr(value))
    try:
        d = Decimal(str(value)).quantize(CENT, rounding=ROUND_HALF_UP)
    except InvalidOperation:
        raise InvalidAmount(repr(value))
    if d <= 0:
        raise InvalidAmount(f"must be positive: {value!r}")
    return d


@dataclass
class Account:
    id: str
    balance: Decimal = Decimal("0.00")
    entries: list[tuple[str, Decimal]] = field(default_factory=list)


class Ledger:
    def __init__(self):
        self._accounts: dict[str, Account] = {}

    def open(self, account_id: str) -> Account:
        acct = Account(account_id)
        self._accounts[account_id] = acct
        return acct

    def get(self, account_id: str) -> Account:
        try:
            return self._accounts[account_id]
        except KeyError:
            raise UnknownAccount(account_id)

    def deposit(self, account_id: str, amount) -> Decimal:
        acct, value = self.get(account_id), money(amount)
        acct.balance += value
        acct.entries.append(("deposit", value))
        return acct.balance

    def withdraw(self, account_id: str, amount) -> Decimal:
        acct, value = self.get(account_id), money(amount)
        if value > acct.balance:
            raise InsufficientFunds(f"{account_id} has {acct.balance}, needs {value}")
        acct.balance -= value
        acct.entries.append(("withdraw", -value))
        return acct.balance

    def transfer(self, from_id: str, to_id: str, amount) -> None:
        src, dst, value = self.get(from_id), self.get(to_id), money(amount)
        if value > src.balance:
            raise InsufficientFunds(f"{from_id} has {src.balance}, needs {value}")
        src.balance -= value
        dst.balance += value
        src.entries.append(("transfer_out", -value))
        dst.entries.append(("transfer_in", value))

    def statement(self, account_id: str) -> list[tuple[str, Decimal, Decimal]]:
        running, out = Decimal("0.00"), []
        for kind, delta in self.get(account_id).entries:
            running += delta
            out.append((kind, delta, running))
        return out
