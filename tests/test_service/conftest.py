import pytest
from pytest_mock import MockerFixture
from sqlalchemy.ext.asyncio import AsyncSession

from api.repository import Repository
from api.service.user import UserService


@pytest.fixture
def repository(mocker: MockerFixture) -> Repository:
    return Repository(session=mocker.create_autospec(spec=AsyncSession))


@pytest.fixture
def user_service(repository: Repository) -> UserService:
    return UserService(repository=repository)
