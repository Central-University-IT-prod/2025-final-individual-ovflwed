from pathlib import Path
from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Query
from pydantic import UUID4

from ad_platform.application.interactors.click_ad import ClickAdInteractor
from ad_platform.application.interactors.get_ad import GetAdInteractor
from ad_platform.presentation.api.schemas.ad import AdClickRequest, AdResponse
from ad_platform.presentation.api.schemas.errors import (
    InvalidRequestResponse,
    NotFoundResponse,
)

router = APIRouter(
    prefix="/ads",
    tags=["Ads"],
    route_class=DishkaRoute,
)


@router.get(
    "",
    summary="Получение рекламного объявления для клиента",
    description="Возвращает рекламное объявление, подходящее для показа клиенту "
    "с учетом таргетинга и ML скора.",
    responses={
        200: {
            "description": "Рекламное объявление успешно получено.",
            "model": AdResponse,
        },
        400: {
            "description": "Некорректные данные запроса.",
            "model": InvalidRequestResponse,
        },
        404: {
            "description": "Клиент или объявление для него не найдено.",
            "model": NotFoundResponse,
        },
    },
)
async def get_ad(
    client_id: Annotated[UUID4, Query(description="UUID клиента.")],
    action: FromDishka[GetAdInteractor],
) -> AdResponse:
    res = await action(client_id)

    return AdResponse(
        ad_id=res.ad_id,
        ad_title=res.ad_title,
        ad_text=res.ad_text,
        advertiser_id=res.advertiser_id,
        image_url=res.image_url,
    )


@router.post(
    "/{ad_id}/click",
    summary="Фиксация перехода по рекламному объявлению",
    description="Фиксирует клик (переход) клиента по рекламному объявлению.",
    status_code=204,
    responses={
        204: {
            "description": "Переход по рекламному объявлению успешно зафиксирован.",
        },
        400: {
            "description": "Некорректные данные запроса.",
            "model": InvalidRequestResponse,
        },
        404: {
            "description": "Рекламное объявление или клиент не найдены.",
            "model": NotFoundResponse,
        },
    },
)
async def click_ad(
    ad_id: Annotated[UUID4, Path(description="UUID рекламного объявления.")],
    body: AdClickRequest,
    action: FromDishka[ClickAdInteractor],
) -> None:
    await action(body.client_id, ad_id)
