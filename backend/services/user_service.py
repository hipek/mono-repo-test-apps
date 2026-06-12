"""User service — business logic for user operations."""

import bcrypt

from models import UserResponse
from repositories import user_repo


def register_user(username: str, password: str, full_name: str | None = None) -> UserResponse:
    """Register a new user with hashed password."""
    if user_repo.exists(username):
        raise ValueError("Username already exists")
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    user = user_repo.create_user(username, hashed, full_name)
    return UserResponse(username=user["username"], full_name=user["full_name"])


def get_user(username: str) -> dict | None:
    """Get user data by username."""
    return user_repo.get_by_username(username)


def verify_password(plain: str, hashed: str) -> bool:
    """Check plain password against hashed."""
    return bcrypt.checkpw(plain.encode(), hashed.encode())
