import abc
import hashlib
import typing

from pydantic import AfterValidator, BaseModel, Field, ValidationInfo
from sqlalchemy import Select

from api import models


def default_order_by(_: bool, info: ValidationInfo) -> bool:  # noqa: FBT001
    """Sets the field's value to True if all other model's fields are False."""
    return not any(info.data.values())


_DefaultOrderBy = typing.Annotated[bool, AfterValidator(default_order_by)]
_OrderBy = bool


class OrderBy[T](BaseModel, abc.ABC):
    """The Default OrderBy clause should always be the last field in the model."""

    def encode(self) -> str:
        return hashlib.md5(self.model_dump_json().encode()).hexdigest()  # noqa: S324

    @abc.abstractmethod
    def apply(self, stmt: Select[tuple[T]]) -> Select[tuple[T]]: ...


class UserOrderBy(OrderBy[models.User]):
    updated_at_asc: _OrderBy = False
    updated_at_desc: _OrderBy = False
    created_at_asc: _OrderBy = False
    created_at_desc: _DefaultOrderBy = Field(default=False, validate_default=True)

    def apply(self, stmt: Select[tuple[models.User]]) -> Select[tuple[models.User]]:
        if self.created_at_desc is True:
            stmt = stmt.order_by(models.User.created_at.desc())
        if self.created_at_asc is True:
            stmt = stmt.order_by(models.User.created_at.asc())
        if self.updated_at_desc is True:
            stmt = stmt.order_by(models.User.updated_at.desc())
        if self.updated_at_asc is True:
            stmt = stmt.order_by(models.User.updated_at.asc())

        return stmt
