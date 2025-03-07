from fastapi import APIRouter

from .common import router as common_router
from .user import router as user_router

router = APIRouter(prefix="/api")

router.include_router(common_router)
router.include_router(user_router)

__all__ = [
    "router",
]
