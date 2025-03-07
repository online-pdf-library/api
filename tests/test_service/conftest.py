import pytest
from pytest_mock import MockerFixture
from sqlalchemy.ext.asyncio import AsyncSession

from api.repository import Repository
from api.service import Service


@pytest.fixture
def repository(mocker: MockerFixture) -> Repository:
    return Repository(session=mocker.create_autospec(spec=AsyncSession))


@pytest.fixture
def service(repository: Repository) -> Service:
    return Service(repository=repository)
