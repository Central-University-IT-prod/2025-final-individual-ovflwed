from typing import Annotated

from pydantic import UUID4, BaseModel, Field


class AdvertiserResponse(BaseModel):
    advertiser_id: Annotated[
        UUID4,
        Field(..., description="Уникальный идентификатор рекламодателя (UUID)."),
    ]
    name: Annotated[
        str,
        Field(..., description="Название рекламодателя.", min_length=1),
    ]

    model_config = {
        "json_schema_extra": {
            "example": {
                "advertiser_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "name": "Booo",
            },
        },
    }


class AdvertiserUpsertRequest(BaseModel):
    advertiser_id: Annotated[
        UUID4,
        Field(..., description="Уникальный идентификатор рекламодателя (UUID)."),
    ]
    name: Annotated[
        str,
        Field(..., description="Название рекламодателя.", min_length=1),
    ]

    model_config = {
        "json_schema_extra": {
            "example": {
                "advertiser_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "name": "Booo",
            },
        },
    }


class MLScoreRequest(BaseModel):
    client_id: Annotated[
        UUID4,
        Field(..., description="Уникальный идентификатор клиента (UUID)."),
    ]
    advertiser_id: Annotated[
        UUID4,
        Field(..., description="Уникальный идентификатор рекламодателя (UUID)."),
    ]
    score: Annotated[
        int,
        Field(..., description="Целочисленное значение ML скора.", ge=0),
    ]

    model_config = {
        "json_schema_extra": {
            "example": {
                "client_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "advertiser_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "score": 0,
            },
        },
    }
