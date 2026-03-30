"""
app/core/exceptions.py
──────────────────────
Centralised custom exception classes and a global exception handler
registered on the FastAPI application.
"""
from __future__ import annotations

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse


class LumoraException(Exception):
    """Base application exception."""
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail: str = "An unexpected error occurred"

    def __init__(self, detail: str | None = None) -> None:
        self.detail = detail or self.__class__.detail
        super().__init__(self.detail)


class NotFoundException(LumoraException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Resource not found"


class ConflictException(LumoraException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Resource already exists"


class ForbiddenException(LumoraException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Action not allowed"


class UnauthorizedException(LumoraException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Authentication required"


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(LumoraException)
    async def lumora_exception_handler(
        request: Request, exc: LumoraException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )
