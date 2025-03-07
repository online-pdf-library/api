from fastapi import APIRouter

router = APIRouter(tags=["Common"])


@router.get("/ping")
def ping() -> str:
    return "pong"
