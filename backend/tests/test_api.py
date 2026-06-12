"""Tests for FastAPI OAuth2 login endpoint."""

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


# ─── Health ───────────────────────────────────────────────────────────


class TestHealth:
    def test_root_returns_ok(self):
        resp = client.get("/")
        assert resp.status_code == 200
        data = resp.json()
        assert data["service"] == "monorepo-api"
        assert data["status"] == "ok"


# ─── Registration ─────────────────────────────────────────────────────


class TestRegister:
    def test_register_new_user(self):
        resp = client.post(
            "/api/register",
            json={
                "username": "newuser",
                "password": "newpass",
                "full_name": "New User",
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["username"] == "newuser"
        assert data["full_name"] == "New User"

    def test_register_duplicate_user(self):
        resp = client.post(
            "/api/register",
            json={
                "username": "admin",
                "password": "somepass",
                "full_name": "Duplicate",
            },
        )
        assert resp.status_code == 409
        assert resp.json()["detail"] == "Username already exists"

    def test_register_missing_password(self):
        resp = client.post(
            "/api/register",
            json={"username": "test", "full_name": "Test"},
        )
        assert resp.status_code == 422


# ─── OAuth2 Token ─────────────────────────────────────────────────────


class TestToken:
    def test_valid_credentials_return_token(self):
        resp = client.post(
            "/api/token",
            data={"username": "admin", "password": "admin123"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["access_token"] is not None
        assert data["token_type"] == "bearer"

    def test_valid_user_credentials(self):
        resp = client.post(
            "/api/token",
            data={"username": "user", "password": "pass123"},
        )
        assert resp.status_code == 200
        assert resp.json()["token_type"] == "bearer"

    def test_invalid_credentials(self):
        resp = client.post(
            "/api/token",
            data={"username": "admin", "password": "wrong"},
        )
        assert resp.status_code == 401
        assert resp.json()["detail"] == "Invalid credentials"

    def test_missing_username(self):
        resp = client.post(
            "/api/token",
            data={"password": "somepass"},
        )
        assert resp.status_code == 422

    def test_missing_password(self):
        resp = client.post(
            "/api/token",
            data={"username": "admin"},
        )
        assert resp.status_code == 422


# ─── Protected Endpoints ──────────────────────────────────────────────


class TestProtected:
    def test_get_me_with_valid_token(self):
        token_resp = client.post(
            "/api/token",
            data={"username": "admin", "password": "admin123"},
        )
        token = token_resp.json()["access_token"]

        resp = client.get("/api/me", headers={"Authorization": f"Bearer {token}"})
        assert resp.status_code == 200
        data = resp.json()
        assert data["username"] == "admin"
        assert data["full_name"] == "Admin User"

    def test_get_me_without_token(self):
        resp = client.get("/api/me")
        assert resp.status_code == 401

    def test_get_me_with_invalid_token(self):
        resp = client.get(
            "/api/me",
            headers={"Authorization": "Bearer invalid-token"},
        )
        assert resp.status_code == 401

    def test_get_me_with_expired_token(self):
        """Token with expired timestamp should be rejected."""
        from config import SECRET_KEY, ALGORITHM
        from jose import jwt
        import time

        payload = {"sub": "admin", "exp": int(time.time()) - 100}
        expired_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        resp = client.get(
            "/api/me",
            headers={"Authorization": f"Bearer {expired_token}"},
        )
        assert resp.status_code == 401
