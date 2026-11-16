import pytest
from fastapi.testclient import TestClient

from txns.app import create_app


@pytest.fixture
def client():
    return TestClient(create_app())


def test_get_transaction(client):
    r = client.get("/transactions/txn_0001")
    assert r.status_code == 200
    assert r.json()["merchant_id"] == "m_acme"


def test_get_unknown_transaction(client):
    assert client.get("/transactions/txn_9999").status_code == 404


def test_create_transaction(client):
    r = client.post("/transactions", json={"merchant_id": "m_acme", "amount": "5.25"})
    assert r.status_code == 201
    assert r.json()["amount"] == "5.25"


def test_create_rejects_bad_amount(client):
    assert client.post("/transactions", json={"merchant_id": "m_acme", "amount": "-1"}).status_code == 400
