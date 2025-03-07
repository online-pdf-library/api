import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from api.repository import Repository
from api.repository.user import UserRepository


@pytest.fixture
def user_repository(db_session: AsyncSession) -> UserRepository:
    return UserRepository(session=db_session)


@pytest.fixture
def repository(db_session: AsyncSession) -> Repository:
    return Repository(session=db_session)
