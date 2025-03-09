import typing

from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm

from api import dependencies, domain
from api.use_case import UseCase

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/sign-up/")
async def sign_up(
    use_case: typing.Annotated[UseCase, Depends(dependencies.get_use_case)],
    data: domain.SignUpData,
    response: Response,
) -> domain.AuthToken:
    return await use_case.auth.sign_up(data=data, response=response)


@router.post("/sign-in/")
async def sign_in(
    use_case: typing.Annotated[UseCase, Depends(dependencies.get_use_case)],
    data: typing.Annotated[OAuth2PasswordRequestForm, Depends()],
    response: Response,
) -> domain.AuthToken:
    return await use_case.auth.sign_in(
        data=domain.SignInData(email=data.username, password=data.password),
        response=response,
    )
