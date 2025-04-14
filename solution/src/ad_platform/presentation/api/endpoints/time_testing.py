from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from ad_platform.application.services.time import TimeService
from ad_platform.presentation.api.schemas.errors import InvalidRequestResponse
from ad_platform.presentation.api.schemas.testing import TimeAdvance

router = APIRouter(
    prefix="/time",
    tags=["Time"],
    route_class=DishkaRoute,
)


@router.post(
    "/advance",
    summary="Установка текущей даты",
    description="Устанавливает текущий день в системе в заданную дату.",
    responses={
        200: {
            "description": "Текущая дата обновлена",
            "model": TimeAdvance,
        },
        400: {
            "description": "Некорректные данные запроса.",
            "model": InvalidRequestResponse,
        },
    },
)
async def advance_time(
    body: TimeAdvance,
    time_service: FromDishka[TimeService],
) -> TimeAdvance:
    return TimeAdvance(current_date=await time_service.advance_time(body.current_date))
