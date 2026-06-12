"""FastAPI app factory."""

from contextlib import asynccontextmanager

import bcrypt
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import init_db
from routes import get_routes

DEMO_USERS = [
    {"username": "admin", "password": "admin123", "full_name": "Admin User"},
    {"username": "user", "password": "pass123", "full_name": "Demo User"},
]


def _seed_demo_users():
    """Insert demo users if database is empty."""
    from database import get_db

    with get_db() as conn:
        count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        if count > 0:
            return
        for u in DEMO_USERS:
            hashed = bcrypt.hashpw(u["password"].encode(), bcrypt.gensalt()).decode()
            conn.execute(
                "INSERT INTO users (username, hashed_password, full_name) VALUES (?, ?, ?)",
                (u["username"], hashed, u["full_name"]),
            )
        conn.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database tables and seed demo users on startup."""
    init_db()
    _seed_demo_users()
    yield


app = FastAPI(title="Monorepo API", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"service": "monorepo-api", "status": "ok"}


app.include_router(get_routes())
