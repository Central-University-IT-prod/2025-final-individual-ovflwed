from typing import Annotated

from pydantic import UUID4, BaseModel, Field

from ad_platform.domain.entities import ClientGender


class ClientResponse(BaseModel):
    client_id: Annotated[
        UUID4,
        Field(..., description="Уникальный идентификатор клиента (UUID)."),
    ]
    login: Annotated[str, Field(..., description="Логин клиента в системе.")]
    age: Annotated[int, Field(..., description="Возраст клиента.")]
    location: Annotated[
        str,
        Field(..., description="Локация клиента (город, регион или район)."),
    ]
    gender: Annotated[
        ClientGender,
        Field(..., description="Пол клиента (MALE или FEMALE)."),
    ]

    model_config = {
        "json_schema_extra": {
            "example": {
                "client_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "login": "string",
                "age": 0,
                "location": "string",
                "gender": "MALE",
            },
        },
    }


class ClientUpsertRequest(BaseModel):
    client_id: Annotated[
        UUID4,
        Field(..., description="Уникальный идентификатор клиента (UUID)."),
    ]
    login: Annotated[
        str,
        Field(..., description="Логин клиента в системе.", min_length=1),
    ]
    age: Annotated[int, Field(..., description="Возраст клиента.", ge=0)]
    location: Annotated[
        str,
        Field(
            ...,
            description="Локация клиента (город, регион или район).",
            min_length=1,
        ),
    ]
    gender: Annotated[
        ClientGender,
        Field(..., description="Пол клиента (MALE или FEMALE)."),
    ]

    model_config = {
        "json_schema_extra": {
            "example": {
                "client_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "login": "string",
                "age": 0,
                "location": "string",
                "gender": "MALE",
            },
        },
    }
