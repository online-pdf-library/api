from fastapi import FastAPI

from .exception import exception_middleware


def add_middlewares(app: FastAPI) -> None:
    app.middleware("http")(exception_middleware)


__all__ = ["add_middlewares"]
