from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Path
from pydantic import UUID4

from ad_platform.application.interactors.create_score import CreateScoreInteractor
from ad_platform.application.services.advertiser import AdvertiserService
from ad_platform.domain.entities import Score
from ad_platform.presentation.api.schemas.adveriser import (
    AdvertiserResponse,
    AdvertiserUpsertRequest,
    MLScoreRequest,
)
from ad_platform.presentation.api.schemas.errors import (
    InvalidRequestResponse,
    NotFoundResponse,
)

router = APIRouter(
    tags=["Advertisers"],
    route_class=DishkaRoute,
)


@router.get(
    "/advertisers/{advertiser_id}",
    summary="Получение рекламодателя по ID",
    description="Возвращает информацию о рекламодателе по его ID.",
    responses={
        200: {
            "description": "Информация о рекламодателе успешно получена.",
            "model": AdvertiserResponse,
        },
        400: {
            "description": "Некорректные данные запроса.",
            "model": InvalidRequestResponse,
        },
        404: {"description": "Рекламодатель не найден.", "model": NotFoundResponse},
    },
)
async def get_advertiser(
    advertiser_id: Annotated[UUID4, Path(description="UUID рекламодателя.")],
    advertiser_service: FromDishka[AdvertiserService],
) -> AdvertiserResponse:
    response = await advertiser_service.get_advertiser(advertiser_id)

    return AdvertiserResponse(
        advertiser_id=response.advertiser_id,
        name=response.name,
    )


@router.post(
    "/advertisers/bulk",
    summary="Массовое создание/обновление рекламодателей",
    description="Создаёт новых или обновляет существующих рекламодателей",
    status_code=201,
    responses={
        201: {
            "description": "Успешное создание/обновление рекламодателей",
            "model": list[AdvertiserResponse],
        },
        400: {
            "description": "Некорректные данные запроса.",
            "model": InvalidRequestResponse,
        },
    },
)
async def create_or_update_advertisers(
    body: list[AdvertiserUpsertRequest],
    advertiser_service: FromDishka[AdvertiserService],
) -> list[AdvertiserResponse]:
    response = await advertiser_service.upsert_advertisers(body)

    return [
        AdvertiserResponse(
            advertiser_id=resp.advertiser_id,
            name=resp.name,
        )
        for resp in response
    ]


@router.post(
    "/ml-scores",
    summary="Добавление или обновление ML скора",
    description="Добавляет или обновляет ML скор для указанной пары клиент-рекламодатель.",
    responses={
        200: {
            "description": "ML скор успешно добавлен или обновлён.",
        },
        400: {
            "description": "Некорректные данные запроса.",
            "model": InvalidRequestResponse,
        },
        404: {
            "description": "Сущность с данным ID не найдена.",
            "model": NotFoundResponse,
        },
    },
)
async def create_or_update_ml_scores(
    body: MLScoreRequest,
    action: FromDishka[CreateScoreInteractor],
) -> None:
    await action(
        Score(
            client_id=body.client_id,
            advertiser_id=body.advertiser_id,
            score=body.score,
        ),
    )
