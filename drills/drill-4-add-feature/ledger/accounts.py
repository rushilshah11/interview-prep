from __future__ import annotations

from dataclasses import dataclass, field
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation

from ledger.errors import DuplicateHold, InsufficientFunds, InvalidAmount, LedgerError, UnknownAccount

CENT = Decimal("0.01")


def money(value) -> Decimal:
    """Convert value (int/str/float/Decimal) to a Decimal rounded to cents; raises InvalidAmount if it is a bool, not numeric, or <= 0."""
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
    """One account: id (str), balance (Decimal), entries (list of (kind, delta)), and holds (hold_id -> held amount)."""
    id: str
    balance: Decimal = Decimal("0.00")
    entries: list[tuple[str, Decimal]] = field(default_factory=list)
    holds: dict[str, Decimal] = field(default_factory=dict)

    @property
    def available(self) -> Decimal:
        """Return balance minus the sum of all active holds (Decimal); computed on read so it can never drift from balance."""
        return self.balance - sum(self.holds.values(), Decimal("0.00"))


class Ledger:
    """In-memory store of accounts keyed by account id."""
    def __init__(self):
        """Create an empty ledger with no accounts."""
        self._accounts: dict[str, Account] = {}

    def open(self, account_id: str) -> Account:
        """Create a zero-balance Account for account_id (str) and return it; no checks, so an existing id is silently overwritten."""
        acct = Account(account_id)
        self._accounts[account_id] = acct
        return acct

    def get(self, account_id: str) -> Account:
        """Return the Account for account_id (str); raises UnknownAccount if it does not exist."""
        try:
            return self._accounts[account_id]
        except KeyError:
            raise UnknownAccount(account_id)

    def deposit(self, account_id: str, amount) -> Decimal:
        """Add amount to account_id, record a "deposit" entry, and return the new balance (Decimal); raises UnknownAccount or InvalidAmount."""
        acct, value = self.get(account_id), money(amount)
        acct.balance += value
        acct.entries.append(("deposit", value))
        return acct.balance

    def withdraw(self, account_id: str, amount) -> Decimal:
        """Subtract amount from account_id, record a "withdraw" entry, and return the new balance (Decimal); raises UnknownAccount, InvalidAmount, or InsufficientFunds if amount > balance."""
        acct, value = self.get(account_id), money(amount)
        if value > acct.available:
            raise InsufficientFunds(f"{account_id} has {acct.balance}, needs {value}")
        acct.balance -= value
        acct.entries.append(("withdraw", -value))
        return acct.balance

    def transfer(self, from_id: str, to_id: str, amount) -> None:
        """Move amount from from_id to to_id, recording transfer_out/transfer_in entries, and return None; raises UnknownAccount for either id, InvalidAmount, or InsufficientFunds if amount > source balance (nothing changes on error)."""
        src, dst, value = self.get(from_id), self.get(to_id), money(amount)
        if value > src.available:
            raise InsufficientFunds(f"{from_id} has {src.balance}, needs {value}")
        src.balance -= value
        dst.balance += value
        src.entries.append(("transfer_out", -value))
        dst.entries.append(("transfer_in", value))

    def statement(self, account_id: str) -> list[tuple[str, Decimal, Decimal]]:
        """Return account_id's history as a list of (kind, delta, running_balance) tuples rebuilt from entries; raises UnknownAccount."""
        running, out = Decimal("0.00"), []
        for kind, delta in self.get(account_id).entries:
            running += delta
            out.append((kind, delta, running))
        return out

    def available(self, account_id: str) -> Decimal:
        """Return account_id's balance minus all active holds (Decimal; equals balance when there are no holds); raises UnknownAccount."""
        return self.get(account_id).available

    def place_hold(self, account_id: str, hold_id: str, amount) -> None:
        """Reserve amount on account_id under hold_id without changing balance; raises UnknownAccount, InvalidAmount, DuplicateHold, or InsufficientFunds if amount > available."""
        acct, value = self.get(account_id), money(amount)
        if hold_id in acct.holds:
            raise DuplicateHold(f"{account_id} already has hold {hold_id}")
        if value > acct.available:
            raise InsufficientFunds(f"{account_id} has {acct.available} available, needs {value}")
        acct.holds[hold_id] = value

    def release_hold(self, account_id: str, hold_id: str) -> None:
        """Cancel hold_id on account_id, returning its amount to available (balance unchanged); raises UnknownAccount, or LedgerError if hold_id is not an active hold."""
        acct = self.get(account_id)
        if hold_id not in acct.holds:
            raise LedgerError(f"{account_id} has no active hold {hold_id}")
        del acct.holds[hold_id]

    def capture_hold(self, account_id: str, hold_id: str, to_id: str) -> None:
        """Settle hold_id on account_id by moving its amount to to_id and removing the hold; raises UnknownAccount for either id, or LedgerError if hold_id is not an active hold (nothing changes on error)."""
        # Error checks (all before any mutation, so capture is all-or-nothing):
        #   1. acct = self.get(account_id)       -> UnknownAccount (source)
        #   2. self.get(to_id)                    -> UnknownAccount (destination), checked BEFORE
        #                                            the hold is touched so a bad to_id can't eat the hold
        #   3. hold_id not in acct.holds          -> LedgerError (unknown, released, or already captured)
        # Logic:
        #   4. value = acct.holds.pop(hold_id)   (remove the hold first: transfer checks available,
        #                                            and the held money only counts as available once
        #                                            the hold is gone; e.g. 100 balance, 80 hold ->
        #                                            available is 20, so transferring 80 would fail)
        #   5. self.transfer(account_id, to_id, value)
        #        - reuses transfer's balance update and its transfer_out / transfer_in entries,
        #          so statement() shows the capture as a normal transfer and stays in sync
        #        - after steps 1-4 this cannot fail: both accounts exist, value already passed
        #          money(), and available >= value because a hold was only placed if it fit
        # Future enhancement (not needed now): wrap step 5 in try/except that restores the hold
        #   (acct.holds[hold_id] = value) and re-raises, in case a later change to transfer adds
        #   a check that could fail after the pop
        acct = self.get(account_id)
        self.get(to_id)
        if hold_id not in acct.holds:
            raise LedgerError(f"{account_id} has no active hold {hold_id}")
        value = acct.holds.pop(hold_id)
        self.transfer(account_id, to_id, value)
