"""Tests for FastAPI login endpoint."""

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestHealth:
    """GET / health check."""

    def test_root_returns_ok(self):
        resp = client.get("/")
        assert resp.status_code == 200
        data = resp.json()
        assert data["service"] == "monorepo-api"
        assert data["status"] == "ok"


class TestLogin:
    """POST /api/login endpoint."""

    def test_valid_admin_credentials(self):
        resp = client.post(
            "/api/login",
            json={"username": "admin", "password": "admin123"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["success"] is True
        assert data["token"] is not None
        assert data["message"] == "Login successful"

    def test_valid_user_credentials(self):
        resp = client.post(
            "/api/login",
            json={"username": "user", "password": "pass123"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["success"] is True
        assert data["token"] is not None

    def test_invalid_credentials_returns_401(self):
        resp = client.post(
            "/api/login",
            json={"username": "admin", "password": "wrong"},
        )
        assert resp.status_code == 401
        assert resp.json()["detail"] == "Invalid credentials"

    def test_empty_body_returns_422(self):
        resp = client.post("/api/login", json={})
        assert resp.status_code == 422

    def test_missing_password_returns_422(self):
        resp = client.post("/api/login", json={"username": "admin"})
        assert resp.status_code == 422
