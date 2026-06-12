from fastapi import APIRouter, Request

from dependencies import get_current_user_from_request
from models import UserResponse

router = APIRouter()


@router.get("/api/me")
def get_me(request: Request):
    user = get_current_user_from_request(request)
    return UserResponse(username=user["username"], full_name=user["full_name"])
