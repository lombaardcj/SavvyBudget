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
