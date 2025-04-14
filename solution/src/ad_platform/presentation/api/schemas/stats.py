from typing import Annotated

from pydantic import BaseModel, Field


class Stats(BaseModel):
    impressions_count: Annotated[
        int,
        Field(
            ...,
            description="Общее количество уникальных показов рекламного объявления.",
        ),
    ]
    clicks_count: Annotated[
        int,
        Field(
            ...,
            description="Общее количество уникальных переходов рекламного объявления.",
        ),
    ]
    conversion: Annotated[
        float,
        Field(..., description="Конверсия рекламного объявления в процентах."),
    ]
    spent_impressions: Annotated[
        float,
        Field(
            ...,
            description="Сумма денег, потраченная на показы рекламного объявления.",
        ),
    ]
    spent_clicks: Annotated[
        float,
        Field(
            ...,
            description="Сумма денег, потраченная на переходы (клики) по рекламному объявлению.",
        ),
    ]
    spent_total: Annotated[
        float,
        Field(
            ...,
            description="Общая сумма денег, потраченная на кампанию (показы и клики).",
        ),
    ]

    model_config = {
        "json_schema_extra": {
            "example": {
                "impressions_count": 0,
                "clicks_count": 0,
                "conversion": 0,
                "spent_impressions": 0,
                "spent_clicks": 0,
                "spent_total": 0,
            },
        },
    }


class DailyStats(Stats):
    date: Annotated[
        int,
        Field(..., description="День (целое число).", ge=0),
    ]

    model_config = {
        "json_schema_extra": {
            "example": {
                "impressions_count": 0,
                "clicks_count": 0,
                "conversion": 0,
                "spent_impressions": 0,
                "spent_clicks": 0,
                "spent_total": 0,
                "date": 0,
            },
        },
    }
