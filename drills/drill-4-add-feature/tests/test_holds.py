from decimal import Decimal

import pytest

from ledger.accounts import Ledger
from ledger.errors import InsufficientFunds, LedgerError


@pytest.fixture
def lg():
    lg = Ledger()
    lg.open("alice")
    lg.open("bob")
    lg.deposit("alice", 100)
    return lg


def test_hold_reduces_available_not_balance(lg):
    lg.place_hold("alice", "h1", 30)
    assert lg.available("alice") == Decimal("70.00")
    assert lg.get("alice").balance == Decimal("100.00")


def test_cannot_hold_more_than_available(lg):
    lg.place_hold("alice", "h1", 80)
    with pytest.raises(InsufficientFunds):
        lg.place_hold("alice", "h2", 21)


def test_withdraw_and_transfer_respect_holds(lg):
    lg.place_hold("alice", "h1", 80)
    with pytest.raises(InsufficientFunds):
        lg.withdraw("alice", 21)
    with pytest.raises(InsufficientFunds):
        lg.transfer("alice", "bob", 21)
    lg.withdraw("alice", 20)


def test_release_hold(lg):
    lg.place_hold("alice", "h1", 30)
    lg.release_hold("alice", "h1")
    assert lg.available("alice") == Decimal("100.00")


def test_capture_hold_moves_money(lg):
    lg.place_hold("alice", "h1", 30)
    lg.capture_hold("alice", "h1", to_id="bob")
    assert lg.get("alice").balance == Decimal("70.00")
    assert lg.available("alice") == Decimal("70.00")
    assert lg.get("bob").balance == Decimal("30.00")


def test_hold_ids_are_unique_and_must_exist(lg):
    lg.place_hold("alice", "h1", 10)
    with pytest.raises(LedgerError):
        lg.place_hold("alice", "h1", 10)
    with pytest.raises(LedgerError):
        lg.release_hold("alice", "nope")
    lg.release_hold("alice", "h1")
    with pytest.raises(LedgerError):
        lg.capture_hold("alice", "h1", to_id="bob")
