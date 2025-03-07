from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api import domain, models
from api.repository.user import UserRepository
from tests import factories


async def test_user_deleted_by_id_successfully(
    db_session: AsyncSession,
    user_repository: UserRepository,
) -> None:
    db_user = await factories.UserFactory.create()

    user = (
        await db_session.execute(select(models.User).where(models.User.id == db_user.id))
    ).scalar_one_or_none()

    assert user is not None

    await user_repository.delete(filter_=domain.UserDeleteFilter(id=db_user.id))

    user = (
        await db_session.execute(select(models.User).where(models.User.id == db_user.id))
    ).scalar_one_or_none()

    assert user is None


async def test_user_deleted_by_email_successfully(
    db_session: AsyncSession,
    user_repository: UserRepository,
) -> None:
    db_user = await factories.UserFactory.create()

    user = (
        await db_session.execute(select(models.User).where(models.User.id == db_user.id))
    ).scalar_one_or_none()

    assert user is not None

    await user_repository.delete(filter_=domain.UserDeleteFilter(email=db_user.email))

    user = (
        await db_session.execute(select(models.User).where(models.User.id == db_user.id))
    ).scalar_one_or_none()

    assert user is None
