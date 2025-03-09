import typing

from fastapi import APIRouter, Depends

from api import dependencies, domain

router = APIRouter(prefix="/user", tags=["User"])


@router.get("/me/", response_model=domain.APIUser)
async def me(
    user: typing.Annotated[domain.User, Depends(dependencies.get_user)],
) -> domain.User:
    return user
