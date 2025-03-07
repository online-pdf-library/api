from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api import domain, models
from tests import factories


async def test_user_factory(db_session: AsyncSession, user: domain.User) -> None:
    await factories.UserFactory.create(**user.model_dump())

    assert (
        await db_session.execute(
            select(models.User).where(
                models.User.id == user.id,
                models.User.email == user.email,
                models.User.password_hash == user.password_hash,
                models.User.timezone == user.timezone,
                models.User.created_at == user.created_at,
                models.User.updated_at == user.updated_at,
            ),
        )
    ).scalar_one_or_none() is not None
