import typing
from contextlib import asynccontextmanager

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.database import Session
from api.repository import Repository
from api.service import Service


@asynccontextmanager
async def get_session() -> typing.AsyncGenerator[AsyncSession, None]:
    session = Session()

    try:
        yield session
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()


@asynccontextmanager
async def get_repository(
    session: typing.Annotated[AsyncSession, Depends(get_session)],
) -> typing.AsyncGenerator[Repository, None]:
    yield Repository(session=session)


@asynccontextmanager
async def get_service(
    repository: typing.Annotated[Repository, Depends(get_repository)],
) -> typing.AsyncGenerator[Service, None]:
    yield Service(repository=repository)
