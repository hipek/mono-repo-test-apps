"""Auth routes — login and registration."""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from models import TokenResponse, UserCreate, UserResponse
from services import token_service, user_service

router = APIRouter()


@router.post("/api/register")
def register(body: UserCreate):
    """Register a new user."""
    try:
        result = user_service.register_user(
            body.username, body.password, body.full_name
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists",
        )
    return result


@router.post("/api/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """OAuth2 password grant — returns JWT access token."""
    user = user_service.get_user(form_data.username)
    if not user or not user_service.verify_password(
        form_data.password, user["hashed_password"]
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = token_service.create_token(form_data.username)
    return token
