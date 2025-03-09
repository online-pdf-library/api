from fastapi import APIRouter, FastAPI

from .auth import router as auth_router
from .common import router as common_router
from .user import router as user_router

router = APIRouter(prefix="/api")

router.include_router(common_router)
router.include_router(user_router)
router.include_router(auth_router)


def include_routers(app: FastAPI) -> None:
    app.include_router(router)


__all__ = [
    "include_routers",
]
