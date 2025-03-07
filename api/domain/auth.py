import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class SignInData(BaseModel):
    email: str
    password: str


class AuthToken(BaseModel):
    token_type: str = Field(default="bearer")
    token: str


class AuthTokenPayload(BaseModel):
    sub: uuid.UUID
    exp: datetime
