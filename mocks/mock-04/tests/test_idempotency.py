import pytest

from payments.errors import IdempotencyConflict
from payments.service import PaymentService


def test_same_key_same_params_returns_original():
    svc = PaymentService()
    a = svc.create("m_1", 25, "USD", idempotency_key="k1")
    b = svc.create("m_1", "25.00", "USD", idempotency_key="k1")
    assert a is b


def test_same_key_different_params_is_rejected():
    svc = PaymentService()
    svc.create("m_1", 25, "USD", idempotency_key="k1")
    with pytest.raises(IdempotencyConflict):
        svc.create("m_1", 26, "USD", idempotency_key="k1")


def test_no_key_creates_new_each_time():
    svc = PaymentService()
    a = svc.create("m_1", 25, "USD")
    b = svc.create("m_1", 25, "USD")
    assert a.id != b.id
