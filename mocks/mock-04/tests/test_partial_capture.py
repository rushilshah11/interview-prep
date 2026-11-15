from decimal import Decimal

import pytest

from payments.errors import InvalidAmount, InvalidTransition, RefundTooLarge
from payments.models import Status
from payments.service import PaymentService


@pytest.fixture
def authorized():
    svc = PaymentService()
    pi = svc.create("m_1", "100.00", "USD")
    svc.confirm(pi.id)
    return svc, pi


def test_capture_less_than_authorized(authorized):
    svc, pi = authorized
    svc.capture(pi.id, "80.00")
    assert pi.status == Status.CAPTURED
    assert pi.captured == Decimal("80.00")


def test_cannot_capture_more_than_authorized(authorized):
    svc, pi = authorized
    with pytest.raises(InvalidAmount):
        svc.capture(pi.id, "100.01")
    assert pi.status == Status.AUTHORIZED


def test_refunds_limited_to_captured_amount(authorized):
    svc, pi = authorized
    svc.capture(pi.id, 80)
    with pytest.raises(RefundTooLarge):
        svc.refund(pi.id, 81)
    svc.refund(pi.id, 80)
    assert pi.status == Status.REFUNDED


def test_partial_capture_is_logged_with_amount(authorized):
    svc, pi = authorized
    svc.capture(pi.id, 80)
    last = svc.events(pi.id)[-1]
    assert (last.to_status, last.amount) == (Status.CAPTURED, Decimal("80.00"))


def test_capture_twice_fails(authorized):
    svc, pi = authorized
    svc.capture(pi.id, 50)
    with pytest.raises(InvalidTransition):
        svc.capture(pi.id, 10)
