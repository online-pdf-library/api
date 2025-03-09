import typing
import uuid

import freezegun
import pytest
from pytest_mock import MockerFixture, MockType

from api import domain, errors, security
from api.repository import Repository
from api.service.user import UserService


@pytest.fixture(autouse=True)
def mocks(mocker: MockerFixture, repository: Repository) -> None:
    mocker.patch.object(repository.user, "get", autospec=True, return_value=None)
    mocker.patch.object(repository.user, "save", autospec=True)
    mocker.patch.object(repository, "transaction", autospec=True)


@pytest.fixture
def create_data(user: domain.User) -> domain.UserCreateData:
    return domain.UserCreateData(
        email=user.email,
        password=user.password_hash,
        timezone=user.timezone,
    )


async def test_error_if_user_with_same_email_exists(
    repository: Repository,
    user_service: UserService,
    create_data: domain.UserCreateData,
    user: domain.User,
) -> None:
    typing.cast(MockType, repository.user.get).return_value = user

    with pytest.raises(errors.AlreadyExistsError):
        await user_service.create(data=create_data)

    typing.cast(MockType, repository.user.get).assert_awaited_once_with(
        filter_=domain.UserGetFilter(email=create_data.email),
    )


@freezegun.freeze_time()
async def test_user_saved_successfully(
    mocker: MockerFixture,
    repository: Repository,
    user_service: UserService,
    create_data: domain.UserCreateData,
) -> None:
    user = domain.User(
        email=create_data.email,
        timezone=create_data.timezone,
        password_hash=security.get_password_hash(password=create_data.password),
    )
    mock_uuid = mocker.patch.object(uuid, "uuid4", return_value=user.id)
    mock_hash = mocker.patch.object(security, "get_password_hash", return_value=user.password_hash)

    await user_service.create(data=create_data)

    typing.cast(MockType, repository.user.save).assert_awaited_once_with(user=user)
    typing.cast(MockType, repository.transaction).assert_called_once()
    mock_uuid.assert_called_once()
    mock_hash.assert_called_once_with(password=create_data.password)
