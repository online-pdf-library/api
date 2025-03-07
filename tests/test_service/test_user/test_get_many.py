import typing

import pytest
from pytest_mock import MockerFixture, MockType

from api import domain, pagination
from api.repository import Repository
from api.service import Service


@pytest.fixture(autouse=True)
def mocks(mocker: MockerFixture, repository: Repository) -> None:
    mocker.patch.object(repository.user, "get_many", autospec=True)


async def test_user_repository_called_with_correct_arguments(
    repository: Repository,
    service: Service,
) -> None:
    filter_ = domain.UserGetManyFilter()
    paging = pagination.PaginationRequest(page=1, page_size=12, fingerprint="fingerprint")
    ordering = domain.UserOrderBy()

    await service.user.get_many(filter_=filter_, paging=paging, ordering=ordering)

    typing.cast(MockType, repository.user.get_many).assert_awaited_once_with(
        filter_=filter_,
        paging=paging,
        ordering=ordering,
    )
