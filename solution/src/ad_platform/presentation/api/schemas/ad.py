from typing import Annotated, Optional

from pydantic import UUID4, BaseModel, Field


class AdResponse(BaseModel):
    ad_id: Annotated[
        UUID4,
        Field(
            ...,
            description="Уникальный идентификатор рекламного объявления "
            "(всегда совпадает с id рекламной кампании).",
        ),
    ]
    ad_title: Annotated[str, Field(..., description="Название рекламного объявления.")]
    ad_text: Annotated[
        str,
        Field(..., description="Текст рекламного объявления, который видит клиент."),
    ]
    advertiser_id: Annotated[
        UUID4,
        Field(..., description="UUID рекламодателя, которому принадлежит объявление."),
    ]
    image_url: Annotated[
        Optional[str],
        Field(
            None,
            description="Ссылка на изображение рекламного объявления, которое видит клиент.",
        ),
    ]

    model_config = {
        "json_schema_extra": {
            "example": {
                "ad_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "ad_title": "string",
                "ad_text": "string",
                "advertiser_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "image_url": "http://glo.api/images/mr-good.png",
            },
        },
    }


class AdClickRequest(BaseModel):
    client_id: Annotated[
        UUID4,
        Field(..., description="Уникальный идентификатор клиента (UUID)."),
    ]

    model_config = {
        "json_schema_extra": {
            "example": {
                "client_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            },
        },
    }
