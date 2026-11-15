from decimal import Decimal

import pytest

from ledger.accounts import Ledger
from ledger.errors import InsufficientFunds, InvalidAmount, UnknownAccount


@pytest.fixture
def lg():
    lg = Ledger()
    lg.open("alice")
    lg.open("bob")
    lg.deposit("alice", 100)
    return lg


def test_deposit_and_withdraw(lg):
    assert lg.withdraw("alice", "30.50") == Decimal("69.50")


def test_withdraw_too_much(lg):
    with pytest.raises(InsufficientFunds):
        lg.withdraw("alice", "100.01")


def test_transfer(lg):
    lg.transfer("alice", "bob", 40)
    assert lg.get("alice").balance == Decimal("60.00")
    assert lg.get("bob").balance == Decimal("40.00")


def test_transfer_too_much_changes_nothing(lg):
    with pytest.raises(InsufficientFunds):
        lg.transfer("alice", "bob", 101)
    assert lg.get("alice").balance == Decimal("100.00")
    assert lg.get("bob").balance == Decimal("0.00")


def test_bad_amounts(lg):
    for bad in (0, -5, "abc", True):
        with pytest.raises(InvalidAmount):
            lg.deposit("alice", bad)


def test_unknown_account(lg):
    with pytest.raises(UnknownAccount):
        lg.deposit("carol", 5)


def test_statement_running_balance(lg):
    lg.withdraw("alice", 10)
    lg.transfer("alice", "bob", 20)
    assert [r[2] for r in lg.statement("alice")] == [Decimal("100.00"), Decimal("90.00"), Decimal("70.00")]
