import typing

import pytest
from pytest_mock import MockerFixture, MockType

from api import domain, errors
from api.repository import Repository
from api.service.user import UserService


@pytest.fixture(autouse=True)
def mocks(mocker: MockerFixture, repository: Repository, user: domain.User) -> None:
    mocker.patch.object(repository.user, "get", autospec=True, return_value=user)
    mocker.patch.object(repository.user, "save", autospec=True)
    mocker.patch.object(repository, "transaction", autospec=True)


@pytest.fixture
def update_data() -> domain.UserUpdateData:
    return domain.UserUpdateData(
        timezone="Europe/Kyiv",
    )


async def test_error_if_user_with_this_id_not_found(
    repository: Repository,
    user_service: UserService,
    update_data: domain.UserUpdateData,
    user: domain.User,
) -> None:
    typing.cast(MockType, repository.user.get).return_value = None

    with pytest.raises(errors.NotFoundError):
        await user_service.update(user_id=user.id, data=update_data)

    typing.cast(MockType, repository.user.get).assert_awaited_once_with(
        filter_=domain.UserGetFilter(id=user.id),
    )


async def test_user_saved_successfully(
    repository: Repository,
    user_service: UserService,
    update_data: domain.UserUpdateData,
    user: domain.User,
) -> None:
    user = user.model_copy(deep=True)
    if "timezone" in update_data:
        user.timezone = update_data["timezone"]

    await user_service.update(user_id=user.id, data=update_data)

    typing.cast(MockType, repository.user.save).assert_awaited_once_with(user=user)
    typing.cast(MockType, repository.transaction).assert_called_once()
