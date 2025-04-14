from typing import Annotated, Optional, Self

from pydantic import UUID4, BaseModel, Field, model_validator

from ad_platform.domain.entities import Gender


class Targeting(BaseModel):
    gender: Annotated[
        Optional[Gender],
        Field(Gender.ALL, description="Пол клиента (MALE, FEMALE и ALL)."),
    ]
    age_from: Annotated[
        Optional[int],
        Field(None, description="Возраст клиента.", ge=0),
    ]
    age_to: Annotated[Optional[int], Field(None, description="Возраст клиента.", ge=0)]
    location: Annotated[
        Optional[str],
        Field(
            None,
            description="Локация клиента (город, регион или район).",
            min_length=1,
        ),
    ]

    @model_validator(mode="after")
    def check_age(self) -> Self:
        if self.age_from and self.age_to and self.age_from > self.age_to:
            raise ValueError

        return self

    model_config = {
        "json_schema_extra": {
            "example": {
                "gender": "MALE",
                "age_from": 14,
                "age_to": 42,
                "location": "52-SAINT-PETERSBURG",
            },
        },
    }


class CampaignCreateRequest(BaseModel):
    impressions_limit: Annotated[
        int,
        Field(..., description="Задаёт лимит показов для рекламного объявления.", ge=0),
    ]
    clicks_limit: Annotated[
        int,
        Field(
            ...,
            description="Задаёт лимит переходов  для рекламного объявления.",
            ge=0,
        ),
    ]
    cost_per_impression: Annotated[
        float,
        Field(..., description="Стоимость одного показа объявления.", ge=0),
    ]
    cost_per_click: Annotated[
        float,
        Field(..., description="Стоимость одного перехода.", ge=0),
    ]
    ad_title: Annotated[
        str,
        Field(..., description="Название рекламного объявления.", min_length=1),
    ]
    ad_text: Annotated[
        str,
        Field(..., description="Текст рекламного объявления.", min_length=1),
    ]
    start_date: Annotated[
        int,
        Field(
            ...,
            description="День начала показа рекламного объявления (включительно).",
            ge=0,
        ),
    ]
    end_date: Annotated[
        int,
        Field(
            ...,
            description="День окончания показа рекламного объявления (включительно).",
            ge=0,
        ),
    ]
    targeting: Annotated[
        Optional[Targeting],
        Field(None, description="Таргетинг рекламного объявления."),
    ]

    @model_validator(mode="after")
    def check_date(self) -> Self:
        if self.start_date > self.end_date:
            raise ValueError

        return self

    model_config = {
        "json_schema_extra": {
            "example": {
                "impressions_limit": 0,
                "clicks_limit": 0,
                "cost_per_impression": 0,
                "cost_per_click": 0,
                "ad_title": "string",
                "ad_text": "string",
                "start_date": 0,
                "end_date": 0,
                "targeting": {
                    "gender": "MALE",
                    "age_from": 0,
                    "age_to": 0,
                    "location": "string",
                },
            },
        },
    }


class CampaignResponse(BaseModel):
    campaign_id: Annotated[
        UUID4,
        Field(..., description="Уникальный идентификатор рекламной кампании (UUID)."),
    ]
    advertiser_id: Annotated[
        UUID4,
        Field(..., description="Уникальный идентификатор рекламодателя (UUID)."),
    ]
    impressions_limit: Annotated[
        int,
        Field(..., ge=0, description="Задаёт лимит показов для рекламного объявления."),
    ]
    clicks_limit: Annotated[
        int,
        Field(
            ...,
            ge=0,
            description="Задаёт лимит переходов  для рекламного объявления.",
        ),
    ]
    cost_per_impression: Annotated[
        float,
        Field(..., ge=0, description="Стоимость одного показа объявления."),
    ]
    cost_per_click: Annotated[
        float,
        Field(..., ge=0, description="Стоимость одного перехода."),
    ]
    ad_title: Annotated[
        str,
        Field(..., min_length=1, description="Название рекламного объявления."),
    ]
    ad_text: Annotated[
        str,
        Field(..., min_length=1, description="Текст рекламного объявления."),
    ]
    start_date: Annotated[
        int,
        Field(
            ...,
            description="День начала показа рекламного объявления (включительно).",
            ge=0,
        ),
    ]
    end_date: Annotated[
        int,
        Field(
            ...,
            description="День окончания показа рекламного объявления (включительно).",
            ge=0,
        ),
    ]
    targeting: Annotated[
        Optional[Targeting],
        Field(None, description="Таргетинг рекламного объявления."),
    ]
    image_url: Annotated[
        Optional[str],
        Field(None, description="Ссылка на изображение рекламного объявления."),
    ]

    model_config = {
        "json_schema_extra": {
            "example": {
                "campaign_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "advertiser_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "impressions_limit": 0,
                "clicks_limit": 0,
                "cost_per_impression": 0,
                "cost_per_click": 0,
                "ad_title": "string",
                "ad_text": "string",
                "start_date": 0,
                "end_date": 0,
                "image_url": None,
                "targeting": {
                    "gender": "MALE",
                    "age_from": 0,
                    "age_to": 0,
                    "location": "string",
                },
            },
        },
    }


class CampaignUpdateRequest(BaseModel):
    impressions_limit: Annotated[
        int,
        Field(
            ...,
            ge=0,
            description="Задаёт лимит показов для рекламного объявления.",
        ),
    ]
    clicks_limit: Annotated[
        int,
        Field(
            ...,
            ge=0,
            description="Задаёт лимит переходов  для рекламного объявления.",
        ),
    ]
    cost_per_impression: Annotated[
        float,
        Field(..., ge=0, description="Стоимость одного показа объявления."),
    ]
    cost_per_click: Annotated[
        float,
        Field(..., ge=0, description="Стоимость одного перехода."),
    ]
    ad_title: Annotated[
        str,
        Field(..., min_length=1, description="Название рекламного объявления."),
    ]
    ad_text: Annotated[
        str,
        Field(..., min_length=1, description="Текст рекламного объявления."),
    ]
    start_date: Annotated[
        int,
        Field(
            ...,
            description="День начала показа рекламного объявления (включительно).",
            ge=0,
        ),
    ]
    end_date: Annotated[
        int,
        Field(
            ...,
            description="День окончания показа рекламного объявления (включительно).",
            ge=0,
        ),
    ]
    targeting: Annotated[
        Optional[Targeting],
        Field(None, description="Таргетинг рекламного объявления."),
    ]

    image_url: Annotated[
        Optional[str],
        Field(..., description="Ссылка на изображение рекламного объявления."),
    ]

    model_config = {
        "json_schema_extra": {
            "example": {
                "impressions_limit": 0,
                "clicks_limit": 0,
                "cost_per_impression": 0,
                "cost_per_click": 0,
                "ad_title": "string",
                "ad_text": "string",
                "start_date": 0,
                "end_date": 0,
                "image_url": None,
                "targeting": {
                    "gender": "MALE",
                    "age_from": 0,
                    "age_to": 0,
                    "location": "string",
                },
            },
        },
    }
