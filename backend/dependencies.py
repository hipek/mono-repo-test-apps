from fastapi import HTTPException, Request, status

from services import token_service, user_service


def get_current_user(token: str) -> dict:
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
    from database import get_db

    with get_db() as conn:
        yield conn


def get_current_user_from_request(request: Request) -> dict:
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid authorization header",
        )
    token = auth.split(" ", 1)[1]
    return get_current_user(token)
