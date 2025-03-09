import contextlib
import typing

from sqlalchemy.ext.asyncio import AsyncSession

from api.repository.user import UserRepository


class Repository:
    def __init__(self, session: AsyncSession) -> None:
        self._s = session

        self.user = UserRepository(session=session)

    @contextlib.asynccontextmanager
    async def transaction(self) -> typing.AsyncGenerator[None, None]:
        t = await self._s.begin_nested()
        try:
            yield
        except:
            await t.rollback()
            raise
        else:
            await t.commit()
