"""Route registration — single router for all routes."""

from fastapi import APIRouter

from routes import auth, users

router = APIRouter()
router.include_router(auth.router)
router.include_router(users.router)


def get_routes() -> APIRouter:
    """Return the combined router with all routes."""
    return router
