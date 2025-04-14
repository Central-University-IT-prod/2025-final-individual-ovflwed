import logging
from functools import partial
from typing import Any

import uvicorn
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from ad_platform.domain.exceptions import (
    AdWasNotShownBeforeError,
    BusinessValidationError,
    NotFoundError,
)
from ad_platform.presentation.api.endpoints import (
    ads,
    advertisers,
    campaigns,
    clients,
    ping,
    stats,
    time_testing,
)
from ad_platform.presentation.api.endpoints.error_handlers import (
    ad_wasnt_shown_exception_handler,
    business_validation_exception_handler,
    not_found_exception_handler,
    validation_exception_handler,
)
from ad_platform.presentation.di import create_container


def create_fastapi_app() -> FastAPI:
    app = FastAPI(docs_url="/docs/")

    # Костыль для удаления ошибки 422 в документации
    _openapi = app.openapi

    def openapi(self: FastAPI) -> dict[str, Any]:
        _openapi()

        for method_item in self.openapi_schema.get("paths").values():
            for param in method_item.values():
                responses = param.get("responses")
                if "422" in responses:
                    del responses["422"]

        return self.openapi_schema

    app.openapi = partial(openapi, app)

    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(NotFoundError, not_found_exception_handler)
    app.add_exception_handler(
        BusinessValidationError,
        business_validation_exception_handler,
    )
    app.add_exception_handler(
        AdWasNotShownBeforeError,
        ad_wasnt_shown_exception_handler,
    )

    app.include_router(router=clients.router)
    app.include_router(router=advertisers.router)
    app.include_router(router=campaigns.router)
    app.include_router(router=ads.router)
    app.include_router(router=stats.router)
    app.include_router(router=time_testing.router)
    app.include_router(router=ping.router)

    return app


def create_app() -> FastAPI:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(process)-7s %(module)-20s %(message)s",
    )
    app = create_fastapi_app()

    container = create_container()

    setup_dishka(container, app)

    return app


if __name__ == "__main__":
    uvicorn.run(create_app(), host="REDACTED", port=8080)
