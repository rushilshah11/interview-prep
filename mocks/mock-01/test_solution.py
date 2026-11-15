from decimal import Decimal

import pytest

from solution import (
    AccountAlreadyExistsError,
    AccountDoesntExistError,
    InvalidAmountError,
    Ledger,
)


@pytest.fixture
def ledger() -> Ledger:
    led = Ledger()
    led.create_account("alice")
    return led


# Happy path

def test_create_deposit_and_get_balance():
    led = Ledger()
    assert led.create_account("alice") == Decimal("0")
    assert led.deposit("alice", 25) == Decimal("25.00")
    assert led.deposit("alice", 10.5) == Decimal("35.50")
    assert led.get_balance("alice") == Decimal("35.50")


# Duplicate account

def test_duplicate_account_raises(ledger):
    ledger.deposit("alice", 5)
    with pytest.raises(AccountAlreadyExistsError):
        ledger.create_account("alice")
    # The existing account must not be reset to zero.
    assert ledger.get_balance("alice") == Decimal("5.00")


# Unknown account

def test_deposit_to_unknown_account_raises(ledger):
    with pytest.raises(AccountDoesntExistError):
        ledger.deposit("bob", 10)


def test_get_balance_of_unknown_account_raises(ledger):
    with pytest.raises(AccountDoesntExistError):
        ledger.get_balance("bob")


# Zero and negative amounts

@pytest.mark.parametrize("amount", [0, 0.0, -1, -0.01, Decimal("-5")])
def test_non_positive_amount_raises(ledger, amount):
    with pytest.raises(InvalidAmountError):
        ledger.deposit("alice", amount)
    assert ledger.get_balance("alice") == Decimal("0")


# More than two decimal places

def test_three_decimal_places_raises(ledger):
    with pytest.raises(InvalidAmountError):
        ledger.deposit("alice", 10.005)
    assert ledger.get_balance("alice") == Decimal("0")


# Float precision

def test_point_one_plus_point_two_is_exactly_point_three(ledger):
    ledger.deposit("alice", 0.1)
    ledger.deposit("alice", 0.2)
    balance = ledger.get_balance("alice")
    assert balance == Decimal("0.30")
    assert str(balance) == "0.30"


# Bool rejected

def test_true_is_rejected(ledger):
    with pytest.raises(TypeError):
        ledger.deposit("alice", True)
    assert ledger.get_balance("alice") == Decimal("0")
