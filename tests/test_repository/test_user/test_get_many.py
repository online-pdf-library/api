from datetime import datetime

import pytz

from api import domain, pagination
from api.repository.user import UserRepository
from tests import factories


async def test_many_users_retrieved_successfully(
    user_repository: UserRepository,
) -> None:
    db_users = await factories.UserFactory.create_batch(3)

    users = await user_repository.get_many(
        filter_=domain.UserGetManyFilter(),
        paging=pagination.PaginationRequest(),
        ordering=domain.UserOrderBy(),
    )

    assert len(users) == len(db_users)
    assert sorted(u.id for u in users) == sorted(u.id for u in db_users)


async def test_many_users_retrieved_with_paging_successfully(
    user_repository: UserRepository,
) -> None:
    db_users = sorted(
        await factories.UserFactory.create_batch(11),
        key=lambda x: x.created_at,
    )
    ordering = domain.UserOrderBy(created_at_asc=True)

    users = await user_repository.get_many(
        filter_=domain.UserGetManyFilter(),
        paging=pagination.PaginationRequest(page=0, page_size=5),
        ordering=ordering,
    )
    assert [u.id for u in users] == [u.id for u in db_users[:5]]
    assert users.paging == pagination.PaginationResponse(
        fingerprint=ordering.encode(),
        page=0,
        page_size=5,
        returned=5,
        total=11,
        max_page=2,
        has_prev_page=False,
        has_next_page=True,
    )

    users = await user_repository.get_many(
        filter_=domain.UserGetManyFilter(),
        paging=pagination.PaginationRequest(
            fingerprint=users.paging.fingerprint,
            page=1,
            page_size=5,
        ),
        ordering=ordering,
    )
    assert [u.id for u in users] == [u.id for u in db_users[5:10]]
    assert users.paging == pagination.PaginationResponse(
        fingerprint=ordering.encode(),
        page=1,
        page_size=5,
        returned=5,
        total=11,
        max_page=2,
        has_prev_page=True,
        has_next_page=True,
    )

    users = await user_repository.get_many(
        filter_=domain.UserGetManyFilter(),
        paging=pagination.PaginationRequest(
            fingerprint=users.paging.fingerprint,
            page=2,
            page_size=5,
        ),
        ordering=ordering,
    )
    assert [u.id for u in users] == [u.id for u in db_users[10:]]
    assert users.paging == pagination.PaginationResponse(
        fingerprint=ordering.encode(),
        page=2,
        page_size=5,
        returned=1,
        total=11,
        max_page=2,
        has_prev_page=True,
        has_next_page=False,
    )


async def test_page_reset_to_zero_on_ordering_change(user_repository: UserRepository) -> None:
    db_users = sorted(
        await factories.UserFactory.create_batch(11),
        key=lambda x: x.created_at,
    )

    ordering = domain.UserOrderBy(created_at_asc=True)

    users = await user_repository.get_many(
        filter_=domain.UserGetManyFilter(),
        paging=pagination.PaginationRequest(page=0, page_size=5),
        ordering=ordering,
    )
    assert [u.id for u in users] == [u.id for u in db_users[:5]]
    assert users.paging == pagination.PaginationResponse(
        fingerprint=ordering.encode(),
        page=0,
        page_size=5,
        returned=5,
        total=11,
        max_page=2,
        has_prev_page=False,
        has_next_page=True,
    )

    ordering = domain.UserOrderBy(created_at_desc=True)

    users = await user_repository.get_many(
        filter_=domain.UserGetManyFilter(),
        paging=pagination.PaginationRequest(
            fingerprint=users.paging.fingerprint,
            page=1,
            page_size=5,
        ),
        ordering=ordering,
    )
    assert [u.id for u in users] == [u.id for u in reversed(db_users[-5:])]
    assert users.paging == pagination.PaginationResponse(
        fingerprint=ordering.encode(),
        page=0,
        page_size=5,
        returned=5,
        total=11,
        max_page=2,
        has_prev_page=False,
        has_next_page=True,
    )


async def test_many_users_retrieved_with_ordering_successfully(
    user_repository: UserRepository,
) -> None:
    datetimes = [datetime(2025, 3, i + 1, tzinfo=pytz.utc) for i in range(3)]
    await factories.UserFactory.create_batch(
        len(datetimes),
        *[
            {"created_at": datetimes[i], "updated_at": datetimes[-(1 + i)]}
            for i in range(len(datetimes))
        ],
    )

    cases = [
        (domain.UserOrderBy(), [2, 1, 0], [0, 1, 2]),
        (domain.UserOrderBy(created_at_desc=True), [2, 1, 0], [0, 1, 2]),
        (domain.UserOrderBy(created_at_asc=True), [0, 1, 2], [2, 1, 0]),
        (domain.UserOrderBy(updated_at_desc=True), [0, 1, 2], [2, 1, 0]),
        (domain.UserOrderBy(updated_at_asc=True), [2, 1, 0], [0, 1, 2]),
    ]

    for ordering, created_at_order, updated_at_order in cases:
        users = await user_repository.get_many(
            filter_=domain.UserGetManyFilter(),
            paging=pagination.PaginationRequest(),
            ordering=ordering,
        )
        for i in range(len(users)):
            assert users[i].created_at == datetimes[created_at_order[i]]
            assert users[i].updated_at == datetimes[updated_at_order[i]]
