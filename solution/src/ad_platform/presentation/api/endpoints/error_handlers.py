from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from ad_platform.domain.exceptions import (
    AdWasNotShownBeforeError,
    BusinessValidationError,
    NotFoundError,
)
from ad_platform.presentation.api.schemas.errors import InvalidRequestResponse


async def validation_exception_handler(
    _: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    return JSONResponse(
        InvalidRequestResponse(detail="Некорректные данные запроса.").model_dump(),
        status_code=400,
    )


async def not_found_exception_handler(
    _: Request,
    exc: NotFoundError,
) -> JSONResponse:
    return JSONResponse(
        InvalidRequestResponse(detail=exc.detail).model_dump(),
        status_code=404,
    )


async def business_validation_exception_handler(
    _: Request,
    exc: BusinessValidationError,
) -> JSONResponse:
    return JSONResponse(
        InvalidRequestResponse(detail=exc.detail).model_dump(),
        status_code=400,
    )


async def ad_wasnt_shown_exception_handler(
    _: Request,
    exc: AdWasNotShownBeforeError,
) -> JSONResponse:
    return JSONResponse(
        InvalidRequestResponse(detail="Реклама не была показана прежде.").model_dump(),
        status_code=400,
    )
