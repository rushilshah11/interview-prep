from decimal import Decimal

import pytest

from wallet.errors import InsufficientFundsError
from wallet.transfers import calculate_fee, transfer
from wallet.wallet import Wallet


@pytest.fixture
def wallets():
    alice, bob, fees = Wallet("alice"), Wallet("bob"), Wallet("fees")
    alice.deposit("USD", 200)
    return alice, bob, fees


def test_small_transfer_pays_minimum_fee():
    assert calculate_fee(Decimal("1.00")) == Decimal("0.01")


def test_fee_is_half_a_percent():
    assert calculate_fee(Decimal("100.00")) == Decimal("0.50")


def test_transfer_moves_money_and_fee(wallets):
    alice, bob, fees = wallets
    fee = transfer(alice, bob, fees, "USD", 100)
    assert fee == Decimal("0.50")
    assert alice.balance("USD") == Decimal("99.50")
    assert bob.balance("USD") == Decimal("100.00")
    assert fees.balance("USD") == Decimal("0.50")


def test_transfer_that_cannot_cover_fee_changes_nothing():
    alice, bob, fees = Wallet("alice"), Wallet("bob"), Wallet("fees")
    alice.deposit("USD", 100.40)  # enough for the amount, not for the 0.50 fee
    with pytest.raises(InsufficientFundsError):
        transfer(alice, bob, fees, "USD", 100)
    assert alice.balance("USD") == Decimal("100.40")
    assert bob.balance("USD") == Decimal("0.00")
    assert fees.balance("USD") == Decimal("0.00")
    assert alice.history(kind="transfer_out") == []
