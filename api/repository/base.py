from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from api import domain, pagination


class BaseRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._s = session

    async def _paginate[T](
        self,
        stmt: Select[tuple[T]],
        paging: pagination.PaginationRequest,
        ordering: domain.OrderBy[T],
    ) -> pagination.Page[T]:
        total_stmt = select(func.count()).select_from(stmt.subquery())
        total = (await self._s.execute(total_stmt)).scalar_one()

        max_page = max(0, (total - 1)) // paging.page_size

        fingerprint = ordering.encode()
        if paging.fingerprint is not None and paging.fingerprint != fingerprint:
            real_page = 0
        else:
            real_page = min(paging.page, max_page)

        stmt = stmt.offset(paging.page_size * real_page).limit(paging.page_size)

        entries = (await self._s.execute(stmt)).scalars().all()

        return pagination.Page(
            entries,
            paging=pagination.PaginationResponse(
                fingerprint=fingerprint,
                page=real_page,
                page_size=paging.page_size,
                returned=len(entries),
                total=total,
                max_page=max_page,
                has_prev_page=real_page > 0,
                has_next_page=total > paging.page_size * real_page + len(entries),
            ),
        )
