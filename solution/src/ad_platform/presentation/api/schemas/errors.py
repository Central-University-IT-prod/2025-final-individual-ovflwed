from pydantic import BaseModel


class NotFoundResponse(BaseModel):
    detail: str

    model_config = {
        "json_schema_extra": {
            "example": {"detail": "Сущность с данным ID не найдена."},
        },
    }


class InvalidRequestResponse(BaseModel):
    detail: str

    model_config = {
        "json_schema_extra": {"example": {"detail": "Некорректные данные запроса."}},
    }
