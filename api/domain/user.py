import typing
import uuid
from datetime import datetime

import pytz
from pydantic import AfterValidator, BaseModel, EmailStr, Field, ValidationInfo

from api.domain.base import DomainModel


def validate_timezone(v: str, _: ValidationInfo) -> str:
    timezone = pytz.timezone(zone=v).zone
    if timezone is None:
        raise ValueError(f'"{v}" is an invalid timezone')
    return timezone


def validate_datetime(v: datetime | None, _: ValidationInfo) -> datetime | None:
    if v is None:
        return None
    if v.tzinfo is None:
        return v.replace(tzinfo=pytz.utc)
    return v.astimezone(tz=pytz.utc)


class User(DomainModel):
    id: uuid.UUID = Field(default_factory=lambda: uuid.uuid4())
    email: EmailStr
    password_hash: str
    timezone: typing.Annotated[str, AfterValidator(validate_timezone)] = "Etc/UTC"
    created_at: typing.Annotated[datetime, AfterValidator(validate_datetime)] = Field(
        default_factory=lambda: datetime.now(pytz.utc),
    )
    updated_at: typing.Annotated[datetime, AfterValidator(validate_datetime)] = Field(
        default_factory=lambda: datetime.now(pytz.utc),
    )


class APIUser(BaseModel):
    id: uuid.UUID
    email: str
    timezone: str
    created_at: datetime
    updated_at: datetime


class UserCreateData(BaseModel):
    email: str
    password_hash: str
    timezone: str


class UserUpdateData(typing.TypedDict):
    timezone: str


class UserGetFilter(typing.TypedDict, total=False):
    id: uuid.UUID
    email: str


class UserGetManyFilter(typing.TypedDict, total=False):
    pass


class UserDeleteFilter(typing.TypedDict, total=False):
    id: uuid.UUID
    email: str
