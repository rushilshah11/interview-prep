from decimal import Decimal

import pytest

from orders.refunds import refund_order
from orders.store import ORDERS, Order, RefundError


@pytest.fixture(autouse=True)
def orders():
    ORDERS.clear()
    ORDERS["o1"] = Order("o1", "c@example.com", Decimal("50.00"), status="paid")
    yield


def test_full_refund():
    assert refund_order("o1") == 50
    assert ORDERS["o1"].status == "refunded"


def test_partial_refund():
    assert refund_order("o1", 20) == 20


def test_refund_more_than_total_fails():
    with pytest.raises(RefundError):
        refund_order("o1", 60)
