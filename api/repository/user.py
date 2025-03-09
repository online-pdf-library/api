from sqlalchemy import delete, select
from sqlalchemy.dialects.postgresql import insert

from api import domain, models, order_by, pagination
from api.repository.base import BaseRepository


class UserRepository(BaseRepository):
    async def save(self, user: domain.User) -> None:
        stmt = insert(models.User).values(self._user_domain_to_model(user).to_dict())

        await self._session.execute(
            stmt.on_conflict_do_update(
                index_elements=["id"],
                set_=dict(stmt.excluded),
            ),
        )

    async def get(self, filter_: domain.UserGetFilter) -> domain.User | None:
        stmt = select(models.User)

        if "id" in filter_:
            stmt = stmt.where(models.User.id == filter_.get("id"))
        if "email" in filter_:
            stmt = stmt.where(models.User.email == filter_.get("email"))

        user = (await self._session.execute(stmt)).scalar_one_or_none()
        return self._user_model_to_domain(user) if user else None

    async def get_many(
        self,
        filter_: domain.UserGetManyFilter,  # noqa: ARG002
        paging: pagination.PaginationRequest,
        ordering: order_by.UserOrderBy,
    ) -> pagination.Page[domain.User]:
        stmt = select(models.User)

        stmt = ordering.apply(stmt)

        users = await self._paginate(stmt, paging=paging, ordering=ordering)
        return pagination.Page(
            [self._user_model_to_domain(user) for user in users],
            paging=users.paging,
        )

    async def delete(self, filter_: domain.UserDeleteFilter) -> None:
        stmt = delete(models.User)

        if "id" in filter_:
            stmt = stmt.where(models.User.id == filter_.get("id"))
        if "email" in filter_:
            stmt = stmt.where(models.User.email == filter_.get("email"))

        await self._session.execute(stmt)

    @staticmethod
    def _user_model_to_domain(user: models.User) -> domain.User:
        return domain.User(
            id=user.id,
            email=user.email,
            password_hash=user.password_hash,
            timezone=user.timezone,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

    @staticmethod
    def _user_domain_to_model(user: domain.User) -> models.User:
        return models.User(
            id=user.id,
            email=user.email,
            password_hash=user.password_hash,
            timezone=user.timezone,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
