from decimal import Decimal

from settlement.fees import fee_for
from settlement.records import parse
from tests.helpers import rec


def test_sale_fee():
    assert fee_for(parse(rec(amount="100.00"))) == Decimal("3.20")


def test_sale_fee_rounds_half_up():
    assert fee_for(parse(rec(amount="15.00"))) == Decimal("0.74")


def test_refund_has_no_fee():
    assert fee_for(parse(rec(type="refund", amount="40"))) == Decimal("0.00")


def test_chargeback_fee_is_flat():
    assert fee_for(parse(rec(type="chargeback", amount="999"))) == Decimal("15.00")
