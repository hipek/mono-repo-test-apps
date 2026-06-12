"""Token repository — SQLite CRUD operations."""

import sqlite3
from database import get_db


def create_token(token: str, username: str, created_at: float, expires_at: float) -> None:
    """Store a token."""
    with get_db() as conn:
        conn.execute(
            "INSERT INTO tokens (token, username, created_at, expires_at) VALUES (?, ?, ?, ?)",
            (token, username, created_at, expires_at),
        )
        conn.commit()


def get_token(token: str) -> dict | None:
    """Get token record. Returns None if not found or expired."""
    with get_db() as conn:
        row = conn.execute("SELECT * FROM tokens WHERE token = ?", (token,)).fetchone()
        if row is None:
            return None
        return dict(row)


def delete_token(token: str) -> None:
    """Remove a token."""
    with get_db() as conn:
        conn.execute("DELETE FROM tokens WHERE token = ?", (token,))
        conn.commit()


def exists(token: str) -> bool:
    """Check if token exists."""
    with get_db() as conn:
        row = conn.execute("SELECT 1 FROM tokens WHERE token = ?", (token,)).fetchone()
        return row is not None
