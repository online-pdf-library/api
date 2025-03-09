import typing
import uuid
from datetime import datetime, timedelta

import jwt
import pytz
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from api import domain
from api.config import config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/sign-in/", auto_error=False)
password_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(password: str, password_hash: str) -> bool:
    return password_ctx.verify(password, password_hash)


def get_password_hash(password: str) -> str:
    return password_ctx.hash(password)


def generate_token(data: dict[str, typing.Any], expire: timedelta) -> str:
    data["exp"] = datetime.now(tz=pytz.utc) + expire
    return jwt.encode(  # type: ignore[reportUnknownMemberType]
        payload=data,
        key=config.auth.secret_key,
        algorithm=config.auth.algorithm,
    )


def decode_token(token: str) -> domain.AuthTokenPayload | None:
    try:
        payload_data: dict[str, typing.Any] = jwt.decode(  # type: ignore[reportUnknownMemberType]
            jwt=token,
            key=config.auth.secret_key,
            algorithms=[config.auth.algorithm],
        )
    except jwt.PyJWTError:
        return None

    try:
        payload = domain.AuthTokenPayload.model_validate(payload_data)
    except ValueError:
        return None

    if datetime.now(tz=pytz.utc) > payload.exp:
        return None

    return payload


def generate_access_token(user_id: uuid.UUID) -> str:
    return generate_token({"sub": str(user_id)}, config.auth.access_token_expire)


def generate_refresh_token(user_id: uuid.UUID) -> str:
    return generate_token({"sub": str(user_id)}, config.auth.refresh_token_expire)
