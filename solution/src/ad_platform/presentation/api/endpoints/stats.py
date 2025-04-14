from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Path
from pydantic import UUID4

from ad_platform.application.interactors.get_advertiser_stats import (
    GetAdvertiserDailyStatsInteractor,
    GetAdvertiserStatsInteractor,
)
from ad_platform.application.interactors.get_campaign_stats import (
    GetCampaignDailyStatsInteractor,
    GetCampaignStatsInteractor,
)
from ad_platform.presentation.api.schemas.errors import (
    InvalidRequestResponse,
    NotFoundResponse,
)
from ad_platform.presentation.api.schemas.stats import DailyStats, Stats

router = APIRouter(
    prefix="/stats",
    tags=["Statistics"],
    route_class=DishkaRoute,
)


@router.get(
    "/campaigns/{campaign_id}",
    summary="Получение статистики по рекламной кампании",
    description="Возвращает агрегированную статистику (показы, переходы, затраты и конверсию) "
    "для заданной рекламной кампании.",
    responses={
        200: {
            "description": "Агрегированная статистика по всем кампаниям рекламодателя"
            " успешно получена.",
            "model": Stats,
        },
        400: {
            "description": "Некорректные данные запроса.",
            "model": InvalidRequestResponse,
        },
        404: {
            "description": "Кампания не найдена.",
            "model": NotFoundResponse,
        },
    },
)
async def get_campaign_stats(
    campaign_id: Annotated[UUID4, Path(description="UUID рекламной кампании.")],
    action: FromDishka[GetCampaignStatsInteractor],
) -> Stats:
    data = await action(campaign_id)
    return Stats(
        clicks_count=data.clicks_count,
        impressions_count=data.impressions_count,
        conversion=data.conversion,
        spent_impressions=data.spent_impressions,
        spent_clicks=data.spent_clicks,
        spent_total=data.spent_total,
    )


@router.get(
    "/advertisers/{advertiser_id}/campaigns",
    summary="Получение статистики по рекламодателю",
    description="Возвращает сводную статистику по всем рекламным кампаниям, "
    "принадлежащим заданному рекламодателю.",
    responses={
        200: {
            "description": "Агрегированная статистика по всем кампаниям рекламодателя "
            "успешно получена.",
            "model": Stats,
        },
        400: {
            "description": "Некорректные данные запроса.",
            "model": InvalidRequestResponse,
        },
        404: {
            "description": "Рекламодатель не найден.",
            "model": NotFoundResponse,
        },
    },
)
async def get_advertiser_stats(
    advertiser_id: Annotated[UUID4, Path(description="UUID рекламодателя.")],
    action: FromDishka[GetAdvertiserStatsInteractor],
) -> Stats:
    data = await action(advertiser_id)
    return Stats(
        clicks_count=data.clicks_count,
        impressions_count=data.impressions_count,
        conversion=data.conversion,
        spent_impressions=data.spent_impressions,
        spent_clicks=data.spent_clicks,
        spent_total=data.spent_total,
    )


@router.get(
    "/campaigns/{campaign_id}/daily",
    summary="Получение ежедневной статистики по рекламной кампании",
    description="Возвращает массив ежедневной статистики для указанной рекламной кампании.",
    responses={
        200: {
            "description": "Ежедневная статистика по всем кампаниям рекламодателя "
            "успешно получена.",
            "model": list[DailyStats],
        },
        400: {
            "description": "Некорректные данные запроса.",
            "model": InvalidRequestResponse,
        },
        404: {
            "description": "Кампания не найдена.",
            "model": NotFoundResponse,
        },
    },
)
async def get_daily_stats(
    campaign_id: Annotated[UUID4, Path(description="UUID рекламной кампании.")],
    action: FromDishka[GetCampaignDailyStatsInteractor],
) -> list[DailyStats]:
    resp = await action(campaign_id)

    return [
        DailyStats(
            clicks_count=data.clicks_count,
            impressions_count=data.impressions_count,
            conversion=data.conversion,
            spent_impressions=data.spent_impressions,
            spent_clicks=data.spent_clicks,
            spent_total=data.spent_total,
            date=data.date,
        )
        for data in resp
    ]


@router.get(
    "/advertisers/{advertiser_id}/daily",
    summary="Получение ежедневной статистики по всем кампаниям рекламодателя",
    description="Возвращает массив ежедневной сводной статистики по всем рекламным кампаниям "
    "заданного рекламодателя.",
    responses={
        200: {
            "description": "Ежедневная статистика по всем кампаниям рекламодателя "
            "успешно получена.",
            "model": list[DailyStats],
        },
        400: {
            "description": "Некорректные данные запроса.",
            "model": InvalidRequestResponse,
        },
        404: {
            "description": "Рекламодатель не найден.",
            "model": NotFoundResponse,
        },
    },
)
async def get_advertiser_daily_stats(
    advertiser_id: Annotated[UUID4, Path(description="UUID рекламодателя.")],
    action: FromDishka[GetAdvertiserDailyStatsInteractor],
) -> list[DailyStats]:
    resp = await action(advertiser_id)

    return [
        DailyStats(
            clicks_count=data.clicks_count,
            impressions_count=data.impressions_count,
            conversion=data.conversion,
            spent_impressions=data.spent_impressions,
            spent_clicks=data.spent_clicks,
            spent_total=data.spent_total,
            date=data.date,
        )
        for data in resp
    ]
