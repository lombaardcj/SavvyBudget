from app.database import init_db
init_db()
from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)

def get_auth_token():
    username = f"envelopeuser_{uuid.uuid4().hex[:8]}"
    password = "envelopepass"
    client.post("/register", json={"username": username, "password": password})
    response = client.post("/token", data={"username": username, "password": password})
    return response.json()["access_token"]

def test_create_envelope():
    token = get_auth_token()
    response = client.post(
        "/envelopes",
        json={"name": "Groceries", "description": "Weekly groceries", "color": "#38bdf8"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Groceries"
    assert data["description"] == "Weekly groceries"
    assert data["color"] == "#38bdf8"

def test_get_envelopes():
    token = get_auth_token()
    response = client.get("/envelopes", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_duplicate_envelope():
    token = get_auth_token()
    envelope_data = {"name": "Groceries", "description": "Weekly groceries", "color": "#38bdf8"}
    # Create the first envelope
    response1 = client.post(
        "/envelopes",
        json=envelope_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response1.status_code == 200
    # Attempt to create a duplicate envelope with the same name
    response2 = client.post(
        "/envelopes",
        json=envelope_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    # Should not be allowed (expect 400 or 409)
    assert response2.status_code in (400, 409)
