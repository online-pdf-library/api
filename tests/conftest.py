import asyncio
import typing

import pytest
from faker import Faker
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from testcontainers.postgres import PostgresContainer

from api import domain, models
from api.database import Session, engine
from tests import factories

faker = Faker()


@pytest.fixture(scope="session", autouse=True)
def event_loop() -> typing.Generator[asyncio.AbstractEventLoop, None, None]:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
def postgres_container() -> typing.Generator[PostgresContainer, None, None]:
    with PostgresContainer(image="postgres:17-alpine") as postgres:
        global engine, Session  # noqa: PLW0603

        engine = create_async_engine(
            url=postgres.get_connection_url(driver="asyncpg"),
            echo=False,
        )
        Session = async_sessionmaker(
            bind=engine,
            autoflush=False,
            expire_on_commit=False,
        )
        yield postgres


@pytest.fixture(autouse=True)
async def db_connection() -> typing.AsyncGenerator[AsyncConnection, None]:
    async with engine.begin() as connection:
        await connection.run_sync(models.Base.metadata.create_all)
        yield connection


@pytest.fixture(autouse=True)
async def db_session(
    db_connection: AsyncConnection,
) -> typing.AsyncGenerator[AsyncSession, None]:
    async with db_connection.begin_nested() as transaction:
        s = Session(bind=db_connection, join_transaction_mode="create_savepoint")
        try:
            yield s
        finally:
            await s.close()
            await transaction.rollback()


@pytest.fixture(autouse=True)
async def before_each(db_session: AsyncSession) -> None:
    factories.setup(session=db_session)


@pytest.fixture
async def user() -> domain.User:
    return domain.User(
        email=faker.email(),
        password_hash=faker.password(),
    )
