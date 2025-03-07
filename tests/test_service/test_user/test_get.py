import typing

import pytest
from pytest_mock import MockerFixture, MockType

from api import domain
from api.repository import Repository
from api.service import Service


@pytest.fixture(autouse=True)
def mocks(mocker: MockerFixture, repository: Repository) -> None:
    mocker.patch.object(repository.user, "get", autospec=True)


async def test_user_repository_called_with_correct_arguments(
    repository: Repository,
    service: Service,
    user: domain.User,
) -> None:
    filter_ = domain.UserGetFilter(id=user.id, email=user.email)

    await service.user.get(filter_=filter_)

    typing.cast(MockType, repository.user.get).assert_awaited_once_with(filter_=filter_)
