"""User repository — SQLite CRUD operations."""

import sqlite3

from database import get_db


def create_user(username: str, hashed_password: str, full_name: str | None) -> dict:
    """Insert a new user. Returns dict with id, username, full_name."""
    with get_db() as conn:
        try:
            conn.execute(
                "INSERT INTO users (username, hashed_password, full_name) VALUES (?, ?, ?)",
                (username, hashed_password, full_name),
            )
            conn.commit()
        except sqlite3.IntegrityError:
            raise ValueError("Username already exists")
        user_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        return {"id": user_id, "username": username, "full_name": full_name}


def get_by_username(username: str) -> dict | None:
    """Get user by username. Returns None if not found."""
    with get_db() as conn:
        row = conn.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()
        if row is None:
            return None
        return dict(row)


def exists(username: str) -> bool:
    """Check if username is taken."""
    with get_db() as conn:
        row = conn.execute(
            "SELECT 1 FROM users WHERE username = ?", (username,)
        ).fetchone()
        return row is not None
