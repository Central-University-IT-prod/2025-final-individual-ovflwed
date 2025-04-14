from typing import Annotated

from pydantic import BaseModel, Field


class TimeAdvance(BaseModel):
    current_date: Annotated[
        int,
        Field(None, description="Текущий день (целое число).", ge=0),
    ]

    model_config = {"json_schema_extra": {"examples": [{"current_date": 1}]}}
