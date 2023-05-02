from typing import Any, Awaitable, Callable

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


class ErrorMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Any], Awaitable[Any]]
    ) -> Response:
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            return JSONResponse(
                content={"error": str(e)},
                status_code=500
            )
