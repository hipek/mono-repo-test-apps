"""User routes — protected endpoints."""

from fastapi import APIRouter, HTTPException, Request, status

from dependencies import get_current_user_from_request
from models import UserResponse

router = APIRouter()


@router.get("/api/me")
def get_me(request: Request):
    """Protected endpoint — requires valid JWT."""
    user = get_current_user_from_request(request)
    return UserResponse(username=user["username"], full_name=user["full_name"])
