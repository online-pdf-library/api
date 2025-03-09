import typing
import uuid
from datetime import datetime

import pytz
from pydantic import BaseModel, EmailStr, Field

from api.config import config
from api.domain import base, validators


class User(base.DomainModel):
    id: uuid.UUID = Field(default_factory=lambda: uuid.uuid4())
    email: EmailStr
    password_hash: str
    timezone: validators.Timezone = config.timezone
    created_at: validators.Datetime = Field(default_factory=lambda: datetime.now(pytz.utc))
    updated_at: validators.Datetime = Field(default_factory=lambda: datetime.now(pytz.utc))


class APIUser(BaseModel):
    id: uuid.UUID
    email: str
    timezone: str
    created_at: datetime
    updated_at: datetime


class UserCreateData(BaseModel):
    email: EmailStr
    password: validators.Password = Field(exclude=True)
    timezone: validators.Timezone = config.timezone


class UserUpdateData(typing.TypedDict, total=False):
    timezone: str


class UserGetFilter(typing.TypedDict, total=False):
    id: uuid.UUID
    email: str


class UserGetManyFilter(typing.TypedDict, total=False):
    pass


class UserDeleteFilter(typing.TypedDict, total=False):
    id: uuid.UUID
    email: str
