from decimal import Decimal

from settlement.report import settle
from tests.helpers import rec


def test_single_merchant_payout():
    r = settle([rec(amount="100.00"), rec(amount="50.00"), rec(type="refund", amount="20.00")])
    ln = r.line("m_1", "USD")
    assert ln.sales == Decimal("150.00")
    assert ln.refunds == Decimal("20.00")
    assert ln.fees == Decimal("4.95")
    assert ln.payout == Decimal("125.05")
    assert not ln.held


def test_currencies_settle_separately():
    r = settle([rec(amount="100", currency="USD"), rec(amount="100", currency="EUR")])
    assert r.line("m_1", "USD").payout == Decimal("96.80")
    assert r.line("m_1", "EUR").payout == Decimal("96.80")


def test_invalid_records_are_reported_not_dropped():
    unknown_type = rec(type="payout")
    zero = rec(amount="0")
    r = settle([rec(), unknown_type, zero])
    assert len(r.lines) == 1
    assert [rid for rid, _ in r.errors] == [unknown_type["id"], zero["id"]]


def test_fees_can_push_merchant_negative_and_hold_payout():
    r = settle([rec(amount="10.00"), rec(type="chargeback", amount="5.00")])
    ln = r.line("m_1", "USD")
    assert ln.held
    assert ln.payout == Decimal("0.00")


def test_only_refunds_is_held():
    r = settle([rec(type="refund", amount="30")])
    assert r.line("m_1", "USD").held
