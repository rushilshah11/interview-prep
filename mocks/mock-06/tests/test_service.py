"""Service-level tests: business rules hold without going through HTTP."""

from decimal import Decimal

import pytest

from errors import InvalidPayment


def test_decimal_amount_is_accepted(service, merchant):
    payment = service.create_payment(merchant.id, Decimal("10.50"), "USD", "k1")
    assert payment.status == "pending"


@pytest.mark.parametrize("amount", [10.5, 0.1 + 0.2, True])
def test_float_or_bool_amount_is_rejected(service, merchant, amount):
    with pytest.raises(InvalidPayment):
        service.create_payment(merchant.id, amount, "USD", "k1")


@pytest.mark.parametrize("amount", ["0", "-1", "10.123", "abc", ""])
def test_invalid_amount_is_rejected(service, merchant, amount):
    with pytest.raises(InvalidPayment):
        service.create_payment(merchant.id, amount, "USD", "k1")


@pytest.mark.parametrize("currency", ["JPY", "usd", ""])
def test_unsupported_currency_is_rejected(service, merchant, currency):
    with pytest.raises(InvalidPayment):
        service.create_payment(merchant.id, "10.00", currency, "k1")
