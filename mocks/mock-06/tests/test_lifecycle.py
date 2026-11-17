"""Service-level tests for capture, fail and refund."""

from decimal import Decimal

import pytest

from errors import InvalidPayment, InvalidTransition, PaymentNotFound, RefundExceedsCaptured
from models import PaymentStatus


@pytest.fixture
def payment(service, merchant):
    """A fresh PENDING payment for 100.00 USD."""
    return service.create_payment(merchant.id, "100.00", "USD", "k1")


@pytest.fixture
def captured(service, payment):
    return service.capture(payment.id)


# --- capture / fail ---------------------------------------------------------

def test_capture_pending_becomes_captured(service, payment):
    assert service.capture(payment.id).status == PaymentStatus.CAPTURED
    assert service.get_payment(payment.id).status == PaymentStatus.CAPTURED


def test_fail_pending_becomes_failed(service, payment):
    assert service.fail(payment.id).status == PaymentStatus.FAILED


def test_capture_twice_is_invalid(service, captured):
    with pytest.raises(InvalidTransition):
        service.capture(captured.id)


def test_capture_failed_is_invalid(service, payment):
    service.fail(payment.id)
    with pytest.raises(InvalidTransition):
        service.capture(payment.id)


def test_fail_captured_is_invalid(service, captured):
    with pytest.raises(InvalidTransition):
        service.fail(captured.id)


@pytest.mark.parametrize("action", ["capture", "fail"])
def test_unknown_payment_is_not_found(service, action):
    with pytest.raises(PaymentNotFound):
        getattr(service, action)("nope")


# --- refund: happy paths ----------------------------------------------------

def test_partial_refund_becomes_partially_refunded(service, captured):
    result = service.refund(captured.id, "30.00")
    assert result.status == PaymentStatus.PARTIALLY_REFUNDED
    assert service.get_refunded_total(captured.id) == Decimal("30.00")


def test_full_refund_becomes_refunded(service, captured):
    assert service.refund(captured.id, "100.00").status == PaymentStatus.REFUNDED


def test_partial_refunds_summing_to_full_become_refunded(service, captured):
    service.refund(captured.id, "40.00")
    result = service.refund(captured.id, "60.00")
    assert result.status == PaymentStatus.REFUNDED
    assert service.get_refunded_total(captured.id) == Decimal("100.00")


# --- refund: rejected, and nothing changes ----------------------------------

def test_two_partial_refunds_exceeding_captured_is_rejected(service, captured):
    service.refund(captured.id, "60.00")
    with pytest.raises(RefundExceedsCaptured):
        service.refund(captured.id, "50.00")
    # Checks ran before writes: the failed refund changed nothing.
    assert service.get_refunded_total(captured.id) == Decimal("60.00")
    assert service.get_payment(captured.id).status == PaymentStatus.PARTIALLY_REFUNDED


def test_single_refund_exceeding_captured_is_rejected(service, captured):
    with pytest.raises(RefundExceedsCaptured):
        service.refund(captured.id, "100.01")
    assert service.get_refunded_total(captured.id) == Decimal("0")
    assert service.get_payment(captured.id).status == PaymentStatus.CAPTURED


def test_refund_pending_is_invalid(service, payment):
    with pytest.raises(InvalidTransition):
        service.refund(payment.id, "10.00")
    assert service.get_refunded_total(payment.id) == Decimal("0")


def test_refund_failed_is_invalid(service, payment):
    service.fail(payment.id)
    with pytest.raises(InvalidTransition):
        service.refund(payment.id, "10.00")


def test_refund_fully_refunded_is_invalid(service, captured):
    service.refund(captured.id, "100.00")
    with pytest.raises(InvalidTransition):
        service.refund(captured.id, "1.00")


@pytest.mark.parametrize("amount", ["0", "-1", "10.123", 10.5])
def test_refund_invalid_amount_is_rejected(service, captured, amount):
    with pytest.raises(InvalidPayment):
        service.refund(captured.id, amount)


def test_refund_unknown_payment_is_not_found(service):
    with pytest.raises(PaymentNotFound):
        service.refund("nope", "10.00")
