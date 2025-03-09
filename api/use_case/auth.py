from fastapi import Request, Response

from api import domain, errors, security
from api.config import config
from api.service import Service


class AuthUseCase:
    def __init__(self, service: Service) -> None:
        self._service = service

    async def sign_up(self, data: domain.SignUpData, response: Response) -> domain.AuthToken:
        user = await self._service.user.create(data=domain.UserCreateData(**data.model_dump()))

        response.set_cookie(
            key=config.auth.refresh_token_cookie_key,
            value=security.generate_refresh_token(user_id=user.id),
        )

        return domain.AuthToken(access_token=security.generate_access_token(user_id=user.id))

    async def sign_in(self, data: domain.SignInData, response: Response) -> domain.AuthToken:
        user = await self._service.user.get(filter_=domain.UserGetFilter(email=data.email))

        if user is None:
            raise errors.NotAuthenticatedError

        if security.verify_password(data.password, user.password_hash) is False:
            raise errors.NotAuthenticatedError

        response.set_cookie(
            key=config.auth.refresh_token_cookie_key,
            value=security.generate_refresh_token(user_id=user.id),
        )

        return domain.AuthToken(access_token=security.generate_access_token(user_id=user.id))

    async def refresh_token(self, request: Request, response: Response) -> domain.AuthToken:
        token = request.cookies.get(config.auth.refresh_token_cookie_key)
        if token is None:
            raise errors.NotAuthenticatedError

        user = await self.authenticate(token=token)

        response.set_cookie(
            key=config.auth.refresh_token_cookie_key,
            value=security.generate_refresh_token(user_id=user.id),
        )

        return domain.AuthToken(access_token=security.generate_access_token(user_id=user.id))

    async def authenticate(self, token: str | None) -> domain.User:
        if token is None:
            raise errors.NotAuthenticatedError

        payload = security.decode_token(token=token)
        if payload is None:
            raise errors.NotAuthenticatedError

        user = await self._service.user.get(filter_=domain.UserGetFilter(id=payload.sub))

        if user is None:
            raise errors.NotAuthenticatedError

        return user
