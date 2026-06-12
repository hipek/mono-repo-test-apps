"""FastAPI dependency providers."""

from fastapi import Depends, HTTPException, Request, status

from services import token_service, user_service


def get_current_user(token: str) -> dict:
    """Validate token and return user dict."""
    user = token_service.validate_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
    user_data = user_service.get_user(user["username"])
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    return {**user_data, "username": user["username"]}


def get_db_session():
    """Yield a database connection."""
    from database import get_db

    with get_db() as conn:
        yield conn


def get_current_user_from_request(request: Request) -> dict:
    """Extract Bearer token from Authorization header and validate."""
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid authorization header",
        )
    token = auth.split(" ", 1)[1]
    return get_current_user(token)
