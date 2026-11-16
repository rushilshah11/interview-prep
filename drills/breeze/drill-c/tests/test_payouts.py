import pytest
from fastapi.testclient import TestClient

from payouts.app import create_app
from payouts.ledger import Ledger


@pytest.fixture
def ledger():
    lg = Ledger()
    lg.add_merchant("acme")
    return lg


@pytest.fixture
def client(ledger):
    return TestClient(create_app(ledger), raise_server_exceptions=False)


def test_payout_sums_succeeded_txns(ledger, client):
    ledger.add_txn("acme", "10.00", "succeeded")
    ledger.add_txn("acme", "5.50", "succeeded")
    r = client.post("/merchants/acme/payouts")
    assert r.status_code == 201
    assert r.json()["amount"] == "15.50"


def test_amount_is_exact_decimal_string(ledger, client):
    ledger.add_txn("acme", "0.10", "succeeded")
    ledger.add_txn("acme", "0.20", "succeeded")
    ledger.add_txn("acme", "1.00", "succeeded")
    assert client.post("/merchants/acme/payouts").json()["amount"] == "1.30"


def test_failed_and_pending_txns_are_not_paid_out(ledger, client):
    ledger.add_txn("acme", "10.00", "succeeded")
    ledger.add_txn("acme", "99.00", "failed")
    ledger.add_txn("acme", "50.00", "pending")
    assert client.post("/merchants/acme/payouts").json()["amount"] == "10.00"


def test_txns_are_not_paid_twice(ledger, client):
    ledger.add_txn("acme", "10.00", "succeeded")
    client.post("/merchants/acme/payouts")
    ledger.add_txn("acme", "3.00", "succeeded")
    assert client.post("/merchants/acme/payouts").json()["amount"] == "3.00"


def test_below_minimum_is_rejected_with_422(ledger, client):
    ledger.add_txn("acme", "0.50", "succeeded")
    r = client.post("/merchants/acme/payouts")
    assert r.status_code == 422
    assert r.json()["error"]["code"] == "below_minimum"


def test_rejected_payout_changes_nothing(ledger, client):
    ledger.add_txn("acme", "0.50", "succeeded")
    client.post("/merchants/acme/payouts")
    ledger.add_txn("acme", "0.75", "succeeded")
    r = client.post("/merchants/acme/payouts")
    assert r.status_code == 201
    assert r.json()["amount"] == "1.25"


def test_unknown_merchant_is_404(client):
    assert client.post("/merchants/nope/payouts").status_code == 404
    assert client.get("/merchants/nope/payouts").status_code == 404
