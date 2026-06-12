"""Pytest fixtures."""

import os
import tempfile

import bcrypt
import pytest

_test_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
os.environ["DATABASE_PATH"] = _test_db.name
_test_db.close()

from database import init_db

DEMO_USERS = [
    {"username": "admin", "password": "admin123", "full_name": "Admin User"},
    {"username": "user", "password": "pass123", "full_name": "Demo User"},
]


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    """Ensure DB tables exist and seed demo users before any test runs."""
    init_db()
    from database import get_db

    with get_db() as conn:
        for u in DEMO_USERS:
            hashed = bcrypt.hashpw(u["password"].encode(), bcrypt.gensalt()).decode()
            conn.execute(
                "INSERT INTO users (username, hashed_password, full_name) VALUES (?, ?, ?)",
                (u["username"], hashed, u["full_name"]),
            )
        conn.commit()
