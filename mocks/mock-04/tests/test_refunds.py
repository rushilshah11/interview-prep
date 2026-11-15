from decimal import Decimal

import pytest

from payments.errors import InvalidTransition, RefundTooLarge
from payments.models import Status
from payments.service import PaymentService


@pytest.fixture
def captured():
    svc = PaymentService()
    pi = svc.create("m_1", "100.00", "USD")
    svc.confirm(pi.id)
    svc.capture(pi.id)
    return svc, pi


def test_partial_refund_stays_captured(captured):
    svc, pi = captured
    svc.refund(pi.id, 30)
    assert pi.status == Status.CAPTURED
    assert pi.refundable == Decimal("70.00")


def test_multiple_partial_refunds_then_full(captured):
    svc, pi = captured
    svc.refund(pi.id, 30)
    svc.refund(pi.id, 50)
    svc.refund(pi.id, 20)
    assert pi.status == Status.REFUNDED
    assert pi.refunded == Decimal("100.00")


def test_refund_more_than_remaining(captured):
    svc, pi = captured
    svc.refund(pi.id, 60)
    with pytest.raises(RefundTooLarge):
        svc.refund(pi.id, "40.01")
    assert pi.refunded == Decimal("60.00")


def test_cannot_refund_uncaptured():
    svc = PaymentService()
    pi = svc.create("m_1", 10, "USD")
    with pytest.raises(InvalidTransition):
        svc.refund(pi.id, 5)
