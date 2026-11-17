import pytest


# --- happy path -------------------------------------------------------------

def test_create_payment_returns_201_pending(client, payload):
    resp = client.post("/payments", json=payload)
    assert resp.status_code == 201
    body = resp.json()
    assert body["status"] == "pending"
    assert body["id"]
    assert body["created_at"]
    assert body["merchant_id"] == payload["merchant_id"]


def test_int_amount_is_accepted(client, payload):
    resp = client.post("/payments", json={**payload, "amount": 10})
    assert resp.status_code == 201


def test_get_payment_returns_created_payment(client, payload):
    created = client.post("/payments", json=payload).json()
    resp = client.get(f"/payments/{created['id']}")
    assert resp.status_code == 200
    assert resp.json() == created


# --- validation (422) -------------------------------------------------------

@pytest.mark.parametrize("field", ["merchant_id", "amount", "currency", "idempotency_key"])
def test_missing_field_is_422(client, payload, field):
    del payload[field]
    resp = client.post("/payments", json=payload)
    assert resp.status_code == 422


def test_non_json_body_is_422(client):
    resp = client.post(
        "/payments", content="not json", headers={"Content-Type": "application/json"}
    )
    assert resp.status_code == 422


@pytest.mark.parametrize("amount", ["0", "-5.00", "10.123", 0, -5])
def test_amount_zero_negative_or_3_decimals_is_422(client, payload, amount):
    resp = client.post("/payments", json={**payload, "amount": amount})
    assert resp.status_code == 422


def test_float_amount_is_422(client, payload):
    resp = client.post("/payments", json={**payload, "amount": 10.5})
    assert resp.status_code == 422


@pytest.mark.parametrize("currency", ["JPY", "usd"])
def test_unsupported_currency_is_422(client, payload, currency):
    resp = client.post("/payments", json={**payload, "currency": currency})
    assert resp.status_code == 422


# --- not found (404) --------------------------------------------------------

def test_unknown_merchant_is_404(client, payload):
    resp = client.post("/payments", json={**payload, "merchant_id": "nope"})
    assert resp.status_code == 404


def test_unknown_payment_is_404(client):
    resp = client.get("/payments/does-not-exist")
    assert resp.status_code == 404


# --- idempotency ------------------------------------------------------------

def test_same_key_same_body_returns_same_payment(client, payload):
    first = client.post("/payments", json=payload)
    second = client.post("/payments", json=payload)
    assert second.status_code == 201
    assert second.json() == first.json()


def test_same_key_different_body_is_409(client, payload):
    client.post("/payments", json=payload)
    resp = client.post("/payments", json={**payload, "amount": "20.00"})
    assert resp.status_code == 409


def test_same_key_equivalent_but_not_exact_amount_is_409(client, payload):
    """Bodies are compared exactly: "10.50" and "10.5" are different."""
    client.post("/payments", json=payload)
    resp = client.post("/payments", json={**payload, "amount": "10.5"})
    assert resp.status_code == 409


def test_same_key_different_merchant_creates_new_payment(client, service, payload):
    other = service.register_merchant("Other")
    first = client.post("/payments", json=payload).json()
    resp = client.post("/payments", json={**payload, "merchant_id": other.id})
    assert resp.status_code == 201
    assert resp.json()["id"] != first["id"]
