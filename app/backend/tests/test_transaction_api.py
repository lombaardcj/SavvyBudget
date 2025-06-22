from app.database import init_db
init_db()

from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)

import datetime

def get_auth_token():
    username = f"transactionuser_{uuid.uuid4().hex[:8]}"
    password = "transactionpass"
    client.post("/register", json={"username": username, "password": password})
    response = client.post("/token", data={"username": username, "password": password})
    return response.json()["access_token"]

def create_envelope(token):
    response = client.post(
        "/envelopes",
        json={"name": "TestEnv", "description": "Test envelope", "color": "#f87171"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    return response.json()["id"]

def test_transaction_crud():
    token = get_auth_token()
    envelope_id = create_envelope(token)

    # Create transaction
    tx_data = {"amount": 42.5, "date": datetime.datetime.now().isoformat(), "description": "Test transaction"}
    response = client.post(
        f"/envelopes/{envelope_id}/transactions",
        json=tx_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    tx = response.json()
    assert tx["amount"] == 42.5
    assert tx["description"] == "Test transaction"
    tx_id = tx["id"]

    # List transactions
    response = client.get(f"/envelopes/{envelope_id}/transactions", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    txs = response.json()
    assert any(t["id"] == tx_id for t in txs)

    # Update transaction
    new_data = {"amount": 99.99, "date": datetime.datetime.now().isoformat(), "description": "Updated transaction"}
    response = client.put(
        f"/envelopes/{envelope_id}/transactions/{tx_id}",
        json=new_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    updated = response.json()
    assert updated["amount"] == 99.99
    assert updated["description"] == "Updated transaction"

    # Delete transaction
    response = client.delete(f"/envelopes/{envelope_id}/transactions/{tx_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["ok"] is True

    # Confirm deletion
    response = client.get(f"/envelopes/{envelope_id}/transactions", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert all(t["id"] != tx_id for t in response.json())

def test_transaction_invalid_envelope():
    token = get_auth_token()
    # Try to create transaction for non-existent envelope
    response = client.post(
        f"/envelopes/999999/transactions",
        json={"amount": 10, "date": datetime.datetime.now().isoformat(), "description": "Invalid env"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Envelope not found"

def test_transaction_invalid_input():
    token = get_auth_token()
    envelope_id = create_envelope(token)
    # Negative amount (should be allowed or not depending on business logic, here we just test API accepts it)
    response = client.post(
        f"/envelopes/{envelope_id}/transactions",
        json={"amount": -100, "date": datetime.datetime.now().isoformat(), "description": "Negative amount"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    # Missing amount (should fail)
    response = client.post(
        f"/envelopes/{envelope_id}/transactions",
        json={"date": datetime.datetime.now().isoformat(), "description": "No amount"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 422

