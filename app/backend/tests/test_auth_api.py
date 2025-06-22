from app.database import init_db
init_db()

from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_register_and_login():
    username = f"testuser_{uuid.uuid4().hex[:8]}"
    password = "testpass"
    response = client.post("/register", json={"username": username, "password": password})
    assert response.status_code == 200
    assert "username" in response.json()
    response = client.post("/token", data={"username": username, "password": password})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_credentials():
    response = client.post("/token", data={"username": "wrong", "password": "wrong"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"
