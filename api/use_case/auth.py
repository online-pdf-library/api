import typing
import uuid
from datetime import datetime

import jwt
import pytz
from starlette.requests import Request

from api import domain, errors, security
from api.config import config
from api.service import Service


class AuthUseCase:
    def __init__(self, service: Service) -> None:
        self._service = service

    async def sign_in(self, data: domain.SignInData) -> domain.AuthToken:
        user = await self._service.user.get(filter_=domain.UserGetFilter(email=data.email))

        if user is None:
            raise errors.NotAuthenticatedError

        if security.verify_password(data.password, user.password_hash) is False:
            raise errors.NotAuthenticatedError

        return self._generate_token(user_id=user.id)

    async def refresh_token(self, user: domain.User) -> domain.AuthToken:
        return self._generate_token(user_id=user.id)

    async def authenticate(self, request: Request | None) -> domain.User:
        payload = self._parse_request(request=request)
        user = await self._service.user.get(filter_=domain.UserGetFilter(id=payload.sub))

        if user is None:
            raise errors.NotAuthenticatedError

        return user

    @staticmethod
    def _parse_request(request: Request | None) -> domain.AuthTokenPayload:
        if not request:
            raise errors.NotAuthenticatedError

        if (authorization := request.headers.get("Authorization")) is None:
            raise errors.NotAuthenticatedError

        try:
            token_type, token = authorization.split(" ")
        except ValueError as e:
            raise errors.NotAuthenticatedError from e

        if token_type.lower() != "bearer":
            raise errors.NotAuthenticatedError

        try:
            payload_data: dict[str, typing.Any] = jwt.decode(  # type: ignore[reportUnknownMemberType]
                jwt=token,
                key=config.auth.secret_key,
                algorithms=[config.auth.algorithm],
            )
        except jwt.PyJWTError as e:
            raise errors.NotAuthenticatedError from e

        try:
            payload = domain.AuthTokenPayload.model_validate(payload_data)
        except ValueError as e:
            raise errors.NotAuthenticatedError from e

        if datetime.now(tz=pytz.utc) > payload.exp:
            raise errors.NotAuthenticatedError

        return payload

    def _generate_token(self, user_id: uuid.UUID) -> domain.AuthToken:
        payload_data: dict[str, typing.Any] = {
            "sub": str(user_id),
            "exp": datetime.now(tz=pytz.utc) + config.auth.token_expire,
        }

        return domain.AuthToken(
            token=str(
                jwt.encode(  # type: ignore[reportUnknownMemberType]
                    payload=payload_data,
                    key=config.auth.secret_key,
                    algorithm=config.auth.algorithm,
                ),
            ),
        )
