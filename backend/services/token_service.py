"""Token service — JWT token creation and validation."""

import time

from jose import JWTError, jwt

from config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from models import TokenResponse
from repositories import token_repo


def create_token(username: str) -> TokenResponse:
    """Create and store a JWT access token."""
    expire = time.time() + ACCESS_TOKEN_EXPIRE_MINUTES * 60
    payload = {"sub": username, "exp": expire}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    token_repo.create_token(token, username, time.time(), expire)
    return TokenResponse(access_token=token)


def validate_token(token: str) -> dict | None:
    """Validate JWT token. Returns user dict with username, or None."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None
    username = payload.get("sub")
    if not username:
        return None
    # Check token exists in store
    if not token_repo.exists(token):
        return None
    # Check not expired
    if payload.get("exp", 0) < time.time():
        token_repo.delete_token(token)
        return None
    return {"username": username}
