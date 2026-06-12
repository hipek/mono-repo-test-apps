"""Pydantic request/response schemas."""

from pydantic import BaseModel


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
