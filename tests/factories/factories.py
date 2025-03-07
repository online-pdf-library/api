import abc
import typing
import uuid

import pytz
from faker import Faker
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from api import models

faker = Faker()


class ModelFactoryAttribute[T]:
    def __init__(self, value: typing.Callable[[], T] | T) -> None:
        self.value = value

    def __call__(self) -> T:
        if callable(self.value):
            return typing.cast(typing.Callable[[], T], self.value)()
        return self.value


class ModelFactory[T: models.Base](abc.ABC):
    __model__: typing.ClassVar[type[T]]  # type: ignore[misc]
    __session__: typing.ClassVar[AsyncSession]

    @classmethod
    def get_attrs(cls) -> dict[str, typing.Any]:
        return {k: v() for k, v in cls.__dict__.items() if isinstance(v, ModelFactoryAttribute)}

    @classmethod
    async def create(cls, **overrides: typing.Any) -> T:
        entity = (
            await cls.__session__.execute(
                insert(cls.__model__)
                .values(**{**cls.get_attrs(), **overrides})
                .returning(cls.__model__),
            )
        ).scalar_one()
        await cls.__session__.commit()

        return entity

    @classmethod
    async def create_batch(
        cls,
        batch_size: int,
        /,
        *overrides: dict[str, typing.Any],
    ) -> list[T]:
        return [
            await cls.create(**(overrides[i] if i < len(overrides) else {}))
            for i in range(batch_size)
        ]


class UserFactory(ModelFactory[models.User]):
    __model__ = models.User

    id = ModelFactoryAttribute(lambda: uuid.uuid4())

    email = ModelFactoryAttribute(lambda: faker.email())
    password_hash = ModelFactoryAttribute(lambda: faker.password())

    timezone = ModelFactoryAttribute("Etc/UTC")

    created_at = ModelFactoryAttribute(lambda: faker.date_time(tzinfo=pytz.utc))
    updated_at = ModelFactoryAttribute(lambda: faker.date_time(tzinfo=pytz.utc))


def setup(session: AsyncSession) -> None:
    UserFactory.__session__ = session
