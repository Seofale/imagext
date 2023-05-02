from fastapi import FastAPI

from .error import ErrorMiddleware


def include_middlewares(app: FastAPI) -> None:
    app.add_middleware(ErrorMiddleware)
