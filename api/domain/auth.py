import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from api.config import config
from api.domain import validators


class SignUpData(BaseModel):
    email: EmailStr
    password: validators.Password
    timezone: validators.Timezone = config.timezone


class SignInData(BaseModel):
    email: EmailStr
    password: validators.Password


class AuthToken(BaseModel):
    access_token: str
    token_type: str = Field(default="bearer")


class AuthTokenPayload(BaseModel):
    sub: uuid.UUID
    exp: datetime
