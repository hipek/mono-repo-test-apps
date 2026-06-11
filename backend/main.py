"""FastAPI backend — OAuth2 login endpoint."""

import secrets
import time
from typing import Annotated

import bcrypt
from fastapi import (
    APIRouter,
    Depends,
    FastAPI,
    HTTPException,
    Request,
    status,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel

# ─── Config ───────────────────────────────────────────────────────────

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
SECRET_KEY = secrets.token_hex(32)

router = APIRouter()

# ─── In-memory user store ─────────────────────────────────────────────

# { username: { "hashed_password": str, "full_name": str } }
users_db: dict[str, dict] = {
    "admin": {
        "hashed_password": bcrypt.hashpw(
            "admin123".encode(), bcrypt.gensalt()
        ).decode(),
        "full_name": "Admin User",
    },
    "user": {
        "hashed_password": bcrypt.hashpw(
            "pass123".encode(), bcrypt.gensalt()
        ).decode(),
        "full_name": "Demo User",
    },
}

# ─── Token store (in-memory) ──────────────────────────────────────────

token_store: dict[str, dict] = {}


# ─── Pydantic models ──────────────────────────────────────────────────


class UserCreate(BaseModel):
    username: str
    password: str
    full_name: str | None = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    username: str
    full_name: str | None


# ─── Helpers ──────────────────────────────────────────────────────────


def _get_user(username: str) -> dict | None:
    return users_db.get(username)


def _verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(
        plain.encode(), hashed.encode()
    )


def _create_access_token(data: dict) -> str:
    expire = time.time() + ACCESS_TOKEN_EXPIRE_MINUTES * 60
    payload = {**data, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def _get_current_user(token: str) -> dict:
    """Extract and validate JWT token, return user dict with username."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    user = _get_user(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    return {**user, "username": username}


# ─── Routes ───────────────────────────────────────────────────────────


@router.get("/")
def root():
    return {"service": "monorepo-api", "status": "ok"}


@router.post("/api/register")
def register(body: UserCreate):
    """Register a new user."""
    if body.username in users_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists",
        )
    users_db[body.username] = {
        "hashed_password": bcrypt.hashpw(
            body.password.encode(), bcrypt.gensalt()
        ).decode(),
        "full_name": body.full_name,
    }
    return UserResponse(username=body.username, full_name=body.full_name)


@router.post("/api/token")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """OAuth2 password grant — returns JWT access token."""
    user = _get_user(form_data.username)
    if not user or not _verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = _create_access_token({"sub": form_data.username})
    token_store[token] = {"username": form_data.username, "created_at": time.time()}
    return TokenResponse(access_token=token)


@router.get("/api/me")
def get_me(request: Request):
    """Protected endpoint — requires valid JWT."""
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid authorization header",
        )
    token = auth.split(" ", 1)[1]
    user = _get_current_user(token)
    return UserResponse(
        username=user["username"],
        full_name=user["full_name"],
    )


# ─── App ──────────────────────────────────────────────────────────────

app = FastAPI(title="Monorepo API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
