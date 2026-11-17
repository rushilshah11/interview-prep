import pytest
from fastapi.testclient import TestClient

from app import app, get_service
from service import PaymentsService


@pytest.fixture
def service():
    return PaymentsService()


@pytest.fixture
def client(service):
    app.dependency_overrides[get_service] = lambda: service
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def merchant(service):
    return service.register_merchant("Acme")


@pytest.fixture
def payload(merchant):
    return {
        "merchant_id": merchant.id,
        "amount": "10.50",
        "currency": "USD",
        "idempotency_key": "key-1",
    }
