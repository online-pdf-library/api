import contextlib

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api import domain, models
from api.repository import Repository


async def test_commit_changes(
    db_session: AsyncSession,
    repository: Repository,
    user: domain.User,
) -> None:
    async with repository.transaction():
        await repository.user.save(user=user)

        assert (
            await db_session.execute(select(models.User).where(models.User.id == user.id))
        ).scalar_one_or_none() is not None

    await db_session.commit()
    await db_session.reset()

    assert (
        await db_session.execute(select(models.User).where(models.User.id == user.id))
    ).scalar_one_or_none() is not None


async def test_rollback_changes_if_exception_thrown(
    db_session: AsyncSession,
    repository: Repository,
    user: domain.User,
) -> None:
    with contextlib.suppress(ValueError):
        async with repository.transaction():
            await repository.user.save(user=user)

            assert (
                await db_session.execute(select(models.User).where(models.User.id == user.id))
            ).scalar_one_or_none() is not None

            raise ValueError

    assert (
        await db_session.execute(select(models.User).where(models.User.id == user.id))
    ).scalar_one_or_none() is None

    await db_session.reset()

    assert (
        await db_session.execute(select(models.User).where(models.User.id == user.id))
    ).scalar_one_or_none() is None
