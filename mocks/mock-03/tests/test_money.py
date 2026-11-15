from decimal import Decimal

import pytest

from wallet.errors import InvalidAmountError, UnsupportedCurrencyError
from wallet.money import to_money, to_positive_money, validate_currency


def test_int_becomes_cents():
    assert to_money(5) == Decimal("5.00")


def test_decimal_is_rounded_half_up():
    assert to_money(Decimal("2.675")) == Decimal("2.68")


def test_float_is_rounded_half_up():
    assert to_money(2.675) == Decimal("2.68")


@pytest.mark.parametrize("bad", [True, "10", None, float("nan"), float("inf")])
def test_rejects_non_numbers(bad):
    with pytest.raises(InvalidAmountError):
        to_money(bad)


@pytest.mark.parametrize("bad", [0, -1, Decimal("-0.01")])
def test_positive_money_rejects_zero_and_negative(bad):
    with pytest.raises(InvalidAmountError):
        to_positive_money(bad)


def test_unknown_currency_rejected():
    with pytest.raises(UnsupportedCurrencyError):
        validate_currency("GBP")
