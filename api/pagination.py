import typing

from pydantic import BaseModel, Field

from api.config import config


class PaginationRequest(BaseModel):
    fingerprint: str | None = None
    page: int = Field(default=0, ge=0)
    page_size: int = Field(
        default=config.pagination.default_page_size,
        ge=config.pagination.min_page_size,
        le=config.pagination.max_page_size,
    )


class PaginationResponse(BaseModel):
    fingerprint: str
    page: int = Field(ge=0)
    page_size: int = Field(
        ge=config.pagination.min_page_size,
        le=config.pagination.max_page_size,
    )
    returned: int = Field(ge=0, le=config.pagination.max_page_size)
    total: int = Field(ge=0)
    max_page: int = Field(ge=0)
    has_prev_page: bool
    has_next_page: bool


class Page[T](list[T]):
    def __init__(self, iterable: typing.Iterable[T], /, paging: PaginationResponse) -> None:
        super().__init__(iterable)
        self.paging = paging
