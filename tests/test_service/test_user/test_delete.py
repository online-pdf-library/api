import typing

import pytest
from pytest_mock import MockerFixture, MockType

from api import domain
from api.repository import Repository
from api.service.user import UserService


@pytest.fixture(autouse=True)
def mocks(mocker: MockerFixture, repository: Repository) -> None:
    mocker.patch.object(repository.user, "delete", autospec=True)
    mocker.patch.object(repository, "transaction", autospec=True)


async def test_user_repository_called_with_correct_arguments(
    repository: Repository,
    user_service: UserService,
    user: domain.User,
) -> None:
    filter_ = domain.UserDeleteFilter(id=user.id, email=user.email)

    await user_service.delete(filter_=filter_)

    typing.cast(MockType, repository.user.delete).assert_awaited_once_with(filter_=filter_)
