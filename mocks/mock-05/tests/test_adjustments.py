from decimal import Decimal

from settlement.fees import fee_for
from settlement.records import parse
from settlement.report import settle
from tests.helpers import rec


def test_adjustment_can_be_negative():
    t = parse(rec(type="adjustment", amount="-12.00"))
    assert t.amount == Decimal("-12.00")


def test_adjustment_has_no_fee():
    assert fee_for(parse(rec(type="adjustment", amount="25"))) == Decimal("0.00")


def test_adjustment_shows_in_report_and_changes_payout():
    r = settle([rec(amount="100.00"), rec(type="adjustment", amount="-10.00"), rec(type="adjustment", amount="2.50")])
    ln = r.line("m_1", "USD")
    assert ln.adjustments == Decimal("-7.50")
    assert ln.payout == Decimal("89.30")


def test_zero_adjustment_is_invalid():
    r = settle([rec(), rec(type="adjustment", amount="0")])
    assert len(r.errors) == 1
