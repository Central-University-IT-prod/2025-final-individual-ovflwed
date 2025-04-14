from dataclasses import asdict
from typing import Annotated, Optional

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, File, Path, Query, UploadFile
from pydantic import UUID4

from ad_platform.application.interactors.create_campaign import CreateCampaignInteractor
from ad_platform.application.interactors.delete_campaign import DeleteCampaignInteractor
from ad_platform.application.interactors.get_campaigns import GetCampaignsInteractor
from ad_platform.application.interactors.update_campaign import (
    UpdateCampaignImageInteractor,
    UpdateCampaignInteractor,
)
from ad_platform.application.services.campaigns import CampaignService
from ad_platform.domain.entities import Campaign, CampaignTarget, Gender
from ad_platform.presentation.api.schemas.campaign import (
    CampaignCreateRequest,
    CampaignResponse,
    CampaignUpdateRequest,
    Targeting,
)
from ad_platform.presentation.api.schemas.errors import (
    InvalidRequestResponse,
    NotFoundResponse,
)

router = APIRouter(
    prefix="/advertisers/{advertiser_id}/campaigns",
    tags=["Campaigns"],
    route_class=DishkaRoute,
)


@router.post(
    "",
    summary="Создание рекламной кампании",
    description="Создаёт новую рекламную кампанию для указанного рекламодателя.",
    status_code=201,
    responses={
        201: {
            "description": "Успешное создание рекламной кампании.",
            "model": CampaignResponse,
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
async def create_campaign(
    advertiser_id: Annotated[UUID4, Path(description="UUID рекламодателя.")],
    body: CampaignCreateRequest,
    action: FromDishka[CreateCampaignInteractor],
) -> CampaignResponse:
    response = await action(
        Campaign(
            advertiser_id=advertiser_id,
            campaign_id=None,
            start_date=body.start_date,
            end_date=body.end_date,
            ad_title=body.ad_title,
            ad_text=body.ad_text,
            impressions_limit=body.impressions_limit,
            clicks_limit=body.clicks_limit,
            cost_per_impression=body.cost_per_impression,
            cost_per_click=body.cost_per_click,
            image_url=None,
            targeting=(
                Targeting(
                    age_from=body.targeting.age_from,
                    age_to=body.targeting.age_to,
                    gender=body.targeting.gender or Gender.ALL,
                    location=body.targeting.location,
                )
                if body.targeting is not None
                else CampaignTarget(Gender.ALL, None, None, None)
            ),
        ),
    )

    return CampaignResponse(**asdict(response))


@router.get(
    "",
    summary="Получение рекламных кампаний рекламодателя с пагинацией",
    description="Возвращает список рекламных кампаний для указанного рекламодателя с пагинацией.",
    responses={
        200: {
            "description": "Список рекламных кампаний рекламодателя.",
            "model": list[CampaignResponse],
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
async def get_campaigns(
    advertiser_id: Annotated[UUID4, Path(description="UUID рекламодателя.")],
    action: FromDishka[GetCampaignsInteractor],
    page: Annotated[Optional[int], Query(description="Номер страницы.", ge=0)] = 0,
    size: Annotated[
        Optional[int],
        Query(description="Количество элементов на странице.", ge=1),
    ] = 10,
) -> list[CampaignResponse]:
    compaigns = await action(advertiser_id, page, size)

    return [CampaignResponse(**asdict(c)) for c in compaigns]


@router.get(
    "/{campaign_id}",
    summary="Получение рекламной кампании по ID",
    description="Возвращает информацию о рекламной кампании по ее ID.",
    responses={
        200: {
            "description": "Кампания успешно получена.",
            "model": CampaignResponse,
        },
        400: {
            "description": "Некорректные данные запроса.",
            "model": InvalidRequestResponse,
        },
        404: {
            "description": "Кампания или рекламодатель не найдены.",
            "model": NotFoundResponse,
        },
    },
)
async def get_campaign(
    advertiser_id: Annotated[UUID4, Path(description="UUID рекламодателя.")],
    campaign_id: Annotated[UUID4, Path(description="UUID рекламной кампании.")],
    campaign_service: FromDishka[CampaignService],
) -> CampaignResponse:
    campaign = await campaign_service.get_campaign(campaign_id, advertiser_id)

    return CampaignResponse(**asdict(campaign))


@router.put(
    "/{campaign_id}",
    summary="Обновление рекламной кампании",
    description="Обновляет разрешённые параметры рекламной кампании до её старта.",
    responses={
        200: {
            "description": "Кампания успешно обновлена.",
            "model": CampaignResponse,
        },
        400: {
            "description": "Некорректные данные запроса.",
            "model": InvalidRequestResponse,
        },
        404: {
            "description": "Кампания или рекламодатель не найдены.",
            "model": NotFoundResponse,
        },
    },
)
async def update_campaign(
    advertiser_id: Annotated[UUID4, Path(description="UUID рекламодателя.")],
    campaign_id: Annotated[UUID4, Path(description="UUID рекламной кампании.")],
    body: CampaignUpdateRequest,
    action: FromDishka[UpdateCampaignInteractor],
) -> CampaignResponse:
    response = await action(
        Campaign(
            campaign_id=campaign_id,
            advertiser_id=advertiser_id,
            start_date=body.start_date,
            end_date=body.end_date,
            ad_title=body.ad_title,
            ad_text=body.ad_text,
            impressions_limit=body.impressions_limit,
            clicks_limit=body.clicks_limit,
            cost_per_impression=body.cost_per_impression,
            cost_per_click=body.cost_per_click,
            image_url=body.image_url,
            targeting=(
                CampaignTarget(
                    age_from=body.targeting.age_from,
                    age_to=body.targeting.age_to,
                    gender=body.targeting.gender,
                    location=body.targeting.location,
                )
                if body.targeting is not None
                else CampaignTarget(Gender.ALL, None, None, None)
            ),
        ),
    )

    return CampaignResponse(
        campaign_id=response.campaign_id,
        advertiser_id=response.advertiser_id,
        impressions_limit=response.impressions_limit,
        clicks_limit=response.clicks_limit,
        cost_per_impression=response.cost_per_impression,
        cost_per_click=response.cost_per_click,
        ad_title=response.ad_title,
        ad_text=response.ad_text,
        start_date=response.start_date,
        end_date=response.end_date,
        image_url=response.image_url,
        targeting=Targeting(
            age_from=response.targeting.age_from,
            age_to=response.targeting.age_to,
            gender=response.targeting.gender,
            location=response.targeting.location,
        ),
    )


@router.delete(
    "/{campaign_id}",
    summary="Удаление рекламной кампании",
    description="Удаляет рекламную кампанию рекламодателя по заданному campaignId.",
    status_code=204,
    responses={
        204: {
            "description": "Кампания успешно удалена.",
        },
        400: {
            "description": "Некорректные данные запроса.",
            "model": InvalidRequestResponse,
        },
        404: {
            "description": "Кампания или рекламодатель не найдены.",
            "model": NotFoundResponse,
        },
    },
)
async def delete_campaign(
    advertiser_id: Annotated[UUID4, Path(description="UUID рекламодателя.")],
    campaign_id: Annotated[UUID4, Path(description="UUID рекламной кампании.")],
    action: FromDishka[DeleteCampaignInteractor],
) -> None:
    await action(campaign_id, advertiser_id)


@router.post(
    "/{campaign_id}/image",
    summary="Добавление или обновление изображения к рекламной кампании",
    description="Загружает изображение в рекламную кампанию рекламодателя по заданному campaignId.",
    responses={
        200: {
            "description": "Изображение успешно загружено.",
        },
        400: {
            "description": "Некорректные данные запроса.",
            "model": InvalidRequestResponse,
        },
        404: {
            "description": "Кампания или рекламодатель не найдены.",
            "model": NotFoundResponse,
        },
    },
)
async def attach_image(
    advertiser_id: Annotated[UUID4, Path(description="UUID рекламодателя.")],
    campaign_id: Annotated[UUID4, Path(description="UUID рекламной кампании.")],
    file: Annotated[UploadFile, File(description="Файл изображения.")],
    action: FromDishka[UpdateCampaignImageInteractor],
) -> None:
    await action(campaign_id, advertiser_id, file.filename, file.file)


@router.delete(
    "/{campaign_id}/image",
    summary="Удаление изображения из рекламной кампании",
    description="Удаляет изображение из рекламной кампании рекламодателя по заданному campaignId.",
    status_code=204,
    responses={
        204: {
            "description": "Изображение успешно удалено.",
        },
        400: {
            "description": "Некорректные данные запроса.",
            "model": InvalidRequestResponse,
        },
        404: {
            "description": "Кампания или рекламодатель не найдены.",
            "model": NotFoundResponse,
        },
    },
)
async def delete_image(
    advertiser_id: Annotated[UUID4, Path(description="UUID рекламодателя.")],
    campaign_id: Annotated[UUID4, Path(description="UUID рекламной кампании.")],
    action: FromDishka[UpdateCampaignImageInteractor],
) -> None:
    await action(campaign_id, advertiser_id, None, None)
