from decimal import Decimal

import pytest

from payments.errors import InvalidAmount, InvalidTransition, NotFound, UnsupportedCurrency
from payments.models import Status
from payments.service import PaymentService


@pytest.fixture
def svc():
    return PaymentService()


def test_create_starts_created(svc):
    pi = svc.create("m_1", "25.00", "USD")
    assert pi.status == Status.CREATED
    assert pi.amount == Decimal("25.00")


def test_create_rejects_bad_input(svc):
    with pytest.raises(InvalidAmount):
        svc.create("m_1", 0, "USD")
    with pytest.raises(UnsupportedCurrency):
        svc.create("m_1", 10, "GBP")


def test_happy_path(svc):
    pi = svc.create("m_1", 40, "USDC")
    svc.confirm(pi.id)
    svc.capture(pi.id)
    assert svc.get(pi.id).status == Status.CAPTURED
    assert pi.captured == Decimal("40.00")


def test_cannot_capture_before_confirm(svc):
    pi = svc.create("m_1", 40, "USD")
    with pytest.raises(InvalidTransition):
        svc.capture(pi.id)


def test_cannot_confirm_twice(svc):
    pi = svc.create("m_1", 40, "USD")
    svc.confirm(pi.id)
    with pytest.raises(InvalidTransition):
        svc.confirm(pi.id)


def test_cancel_before_capture(svc):
    pi = svc.create("m_1", 40, "USD")
    svc.confirm(pi.id)
    svc.cancel(pi.id)
    assert pi.status == Status.CANCELED


def test_cannot_cancel_after_capture(svc):
    pi = svc.create("m_1", 40, "USD")
    svc.confirm(pi.id)
    svc.capture(pi.id)
    with pytest.raises(InvalidTransition):
        svc.cancel(pi.id)
    assert pi.status == Status.CAPTURED


def test_unknown_intent(svc):
    with pytest.raises(NotFound):
        svc.confirm("pi_999")


def test_failed_transition_is_not_logged(svc):
    pi = svc.create("m_1", 40, "USD")
    with pytest.raises(InvalidTransition):
        svc.capture(pi.id)
    assert svc.events(pi.id) == []


def test_events_record_each_change(svc):
    pi = svc.create("m_1", 40, "USD")
    svc.confirm(pi.id)
    svc.capture(pi.id)
    assert [(e.from_status, e.to_status) for e in svc.events(pi.id)] == [
        (Status.CREATED, Status.AUTHORIZED),
        (Status.AUTHORIZED, Status.CAPTURED),
    ]
