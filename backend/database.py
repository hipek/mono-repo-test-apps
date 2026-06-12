"""SQLite database setup and helpers."""

import sqlite3
import os
from contextlib import contextmanager

from config import DATABASE_PATH


def _get_conn() -> sqlite3.Connection:
    """Create or connect to the SQLite database."""
    if DATABASE_PATH != ":memory:":
        os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Create tables if they don't exist."""
    conn = _get_conn()
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                hashed_password TEXT NOT NULL,
                full_name TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tokens (
                token TEXT PRIMARY KEY,
                username TEXT NOT NULL,
                created_at REAL NOT NULL,
                expires_at REAL NOT NULL
            )
        """)
        conn.commit()
    finally:
        conn.close()


@contextmanager
def get_db():
    """Yield a database connection, auto-close."""
    conn = _get_conn()
    try:
        yield conn
    finally:
        conn.close()
