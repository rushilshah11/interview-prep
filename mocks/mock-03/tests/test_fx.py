from decimal import Decimal

import pytest

from wallet.errors import InsufficientFundsError, MissingRateError
from wallet.fx import convert
from wallet.wallet import Wallet


@pytest.fixture
def wallet() -> Wallet:
    w = Wallet("alice")
    w.deposit("USD", 100)
    return w


def test_convert_usd_to_eur(wallet):
    credited = convert(wallet, "USD", "EUR", 50)
    assert credited == Decimal("46.00")
    assert wallet.balance("USD") == Decimal("50.00")
    assert wallet.balance("EUR") == Decimal("46.00")


def test_convert_rounds_half_up_to_cents(wallet):
    # 10.01 * 0.92 = 9.2092 -> 9.21
    assert convert(wallet, "USD", "EUR", 10.01) == Decimal("9.21")


def test_convert_records_history(wallet):
    convert(wallet, "USD", "EUR", 50)
    assert [t.kind for t in wallet.history(kind="convert_out")] == ["convert_out"]
    assert wallet.history(kind="convert_in")[0].amount == Decimal("46.00")


def test_missing_rate_changes_nothing(wallet):
    with pytest.raises(MissingRateError):
        convert(wallet, "USD", "EUR", 50, rates={})
    assert wallet.balance("USD") == Decimal("100.00")
    assert wallet.balance("EUR") == Decimal("0.00")


def test_insufficient_funds_changes_nothing(wallet):
    with pytest.raises(InsufficientFundsError):
        convert(wallet, "USD", "EUR", 500)
    assert wallet.balance("USD") == Decimal("100.00")
    assert wallet.balance("EUR") == Decimal("0.00")
