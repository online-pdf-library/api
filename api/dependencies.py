import typing

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api import domain, security
from api.database import Session
from api.repository import Repository
from api.service import Service
from api.use_case import UseCase


async def get_session() -> typing.AsyncGenerator[AsyncSession, None]:
    session = Session()

    try:
        yield session
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.commit()
        await session.close()


async def get_repository(
    session: typing.Annotated[AsyncSession, Depends(get_session)],
) -> typing.AsyncGenerator[Repository, None]:
    yield Repository(session=session)


async def get_service(
    repository: typing.Annotated[Repository, Depends(get_repository)],
) -> typing.AsyncGenerator[Service, None]:
    yield Service(repository=repository)


async def get_use_case(
    service: typing.Annotated[Service, Depends(get_service)],
) -> typing.AsyncGenerator[UseCase, None]:
    yield UseCase(service=service)


async def get_user(
    token: typing.Annotated[str | None, Depends(security.oauth2_scheme)],
    use_case: typing.Annotated[UseCase, Depends(get_use_case)],
) -> typing.AsyncGenerator[domain.User, None]:
    yield await use_case.auth.authenticate(token=token)


async def get_optional_user(
    token: typing.Annotated[str | None, Depends(security.oauth2_scheme)],
    use_case: typing.Annotated[UseCase, Depends(get_use_case)],
) -> typing.AsyncGenerator[domain.User | None, None]:
    if token is None:
        yield None
    yield await use_case.auth.authenticate(token=token)
