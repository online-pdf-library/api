import uuid

from api import domain, errors, order_by, pagination, security
from api.repository import Repository


class UserService:
    def __init__(self, repository: Repository) -> None:
        self._repo = repository

    async def create(self, data: domain.UserCreateData) -> domain.User:
        user = await self._repo.user.get(filter_=domain.UserGetFilter(email=data.email))
        if user is not None:
            raise errors.AlreadyExistsError

        user = domain.User(
            **data.model_dump(),
            password_hash=security.get_password_hash(password=data.password),
        )

        async with self._repo.transaction():
            await self._repo.user.save(user=user)

        return user

    async def update(self, user_id: uuid.UUID, data: domain.UserUpdateData) -> domain.User:
        user = await self._repo.user.get(filter_=domain.UserGetFilter(id=user_id))
        if user is None:
            raise errors.NotFoundError

        user.model_update(data)

        async with self._repo.transaction():
            await self._repo.user.save(user=user)

        return user

    async def get(self, filter_: domain.UserGetFilter) -> domain.User | None:
        return await self._repo.user.get(filter_=filter_)

    async def get_many(
        self,
        filter_: domain.UserGetManyFilter,
        paging: pagination.PaginationRequest,
        ordering: order_by.UserOrderBy,
    ) -> pagination.Page[domain.User]:
        return await self._repo.user.get_many(filter_=filter_, paging=paging, ordering=ordering)

    async def delete(self, filter_: domain.UserDeleteFilter) -> None:
        async with self._repo.transaction():
            await self._repo.user.delete(filter_=filter_)
