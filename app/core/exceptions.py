
import logging

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from app.core.response import ErrorDetail, ResponseInfo


logger = logging.getLogger(__name__)


class AppException(Exception):
    def __init__(
        self,
        message: str,
        status_code: int = 400,
        code: str = "APPLICATION_ERROR",
        field: str | None = None,
    ):
        self.message = message
        self.status_code = status_code
        self.code = code
        self.field = field
        super().__init__(message)


def error_response(
    message: str,
    status_code: int,
    errors: list[ErrorDetail] | None = None,
) -> JSONResponse:

    response = ResponseInfo[None](
        success=False,
        message=message,
        status_code=status_code,
        data=None,
        errors=errors,
    )

    return JSONResponse(
        status_code=status_code,
        content=response.model_dump(mode="json"),
    )


def register_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(AppException)
    async def application_exception_handler(
        request: Request,
        exc: AppException,
    ):
        return error_response(
            message=exc.message,
            status_code=exc.status_code,
            errors=[
                ErrorDetail(
                    code=exc.code,
                    message=exc.message,
                    field=exc.field,
                )
            ],
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(
        request: Request,
        exc: HTTPException,
    ):
        message = (
            exc.detail
            if isinstance(exc.detail, str)
            else "Request failed"
        )

        return error_response(
            message=message,
            status_code=exc.status_code,
            errors=[
                ErrorDetail(
                    code=f"HTTP_{exc.status_code}",
                    message=message,
                )
            ],
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError,
    ):
        errors = [
            ErrorDetail(
                code=error["type"],
                message=error["msg"],
                field=".".join(
                    str(part) for part in error["loc"]
                ),
            )
            for error in exc.errors()
        ]

        return error_response(
            message="Request validation failed",
            status_code=422,
            errors=errors,
        )

    @app.exception_handler(SQLAlchemyError)
    async def database_exception_handler(
        request: Request,
        exc: SQLAlchemyError,
    ):
        logger.exception(
            "Database operation failed",
            exc_info=exc,
        )

        return error_response(
            message="A database error occurred",
            status_code=500,
            errors=[
                ErrorDetail(
                    code="DATABASE_ERROR",
                    message="Unable to process the database operation",
                )
            ],
        )

    @app.exception_handler(Exception)
    async def unexpected_exception_handler(
        request: Request,
        exc: Exception,
    ):
        logger.exception(
            "Unexpected application error",
            exc_info=exc,
        )

        return error_response(
            message="Internal server error",
            status_code=500,
            errors=[
                ErrorDetail(
                    code="INTERNAL_SERVER_ERROR",
                    message="Something went wrong. Please try again later.",
                )
            ],
        )
