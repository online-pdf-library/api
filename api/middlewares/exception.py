import typing

from fastapi import Request, Response
from fastapi.responses import JSONResponse

from api import errors


async def exception_middleware(
    request: Request,
    call_next: typing.Callable[[Request], typing.Awaitable[Response]],
) -> Response:
    try:
        response = await call_next(request)
    except errors.VisibleError as e:
        return JSONResponse(content={"detail": str(e)}, status_code=e.status_code())

    return response
