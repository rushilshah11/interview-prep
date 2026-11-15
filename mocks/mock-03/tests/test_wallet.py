from decimal import Decimal

import pytest

from wallet.errors import InsufficientFundsError, InvalidAmountError, UnsupportedCurrencyError
from wallet.wallet import Wallet


@pytest.fixture
def wallet() -> Wallet:
    return Wallet("alice")


def test_new_wallet_starts_empty(wallet):
    assert wallet.balance("USD") == Decimal("0.00")
    assert wallet.balance("EUR") == Decimal("0.00")


def test_deposit_and_withdraw(wallet):
    assert wallet.deposit("USD", 50) == Decimal("50.00")
    assert wallet.withdraw("USD", 20) == Decimal("30.00")
    assert wallet.balance("USD") == Decimal("30.00")


def test_currencies_are_separate(wallet):
    wallet.deposit("USD", 10)
    assert wallet.balance("USDC") == Decimal("0.00")


def test_float_deposit_rounds_half_up(wallet):
    wallet.deposit("USD", 1.005)
    assert wallet.balance("USD") == Decimal("1.01")


def test_withdraw_entire_balance(wallet):
    wallet.deposit("EUR", 40)
    assert wallet.withdraw("EUR", 40) == Decimal("0.00")


def test_overdraft_rejected_and_balance_unchanged(wallet):
    wallet.deposit("USD", 10)
    with pytest.raises(InsufficientFundsError):
        wallet.withdraw("USD", 10.01)
    assert wallet.balance("USD") == Decimal("10.00")


def test_unsupported_currency(wallet):
    with pytest.raises(UnsupportedCurrencyError):
        wallet.deposit("GBP", 10)


def test_non_positive_deposit(wallet):
    with pytest.raises(InvalidAmountError):
        wallet.deposit("USD", 0)


def test_history_filters(wallet):
    wallet.deposit("USD", 10)
    wallet.deposit("EUR", 5)
    wallet.withdraw("USD", 3)
    assert [t.kind for t in wallet.history()] == ["deposit", "deposit", "withdrawal"]
    assert [t.amount for t in wallet.history(currency="USD")] == [Decimal("10.00"), Decimal("3.00")]
    assert len(wallet.history(kind="withdrawal")) == 1
    assert wallet.history(currency="USD")[-1].balance_after == Decimal("7.00")
