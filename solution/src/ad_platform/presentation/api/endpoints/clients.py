from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Path
from pydantic import UUID4

from ad_platform.application.services.client import ClientService
from ad_platform.presentation.api.schemas.client import (
    ClientResponse,
    ClientUpsertRequest,
)
from ad_platform.presentation.api.schemas.errors import (
    InvalidRequestResponse,
    NotFoundResponse,
)

router = APIRouter(
    prefix="/clients",
    tags=["Clients"],
    route_class=DishkaRoute,
)


@router.get(
    "/{client_id}",
    summary="Получение клиента по ID",
    description="Возвращает информацию о клиенте по его ID.",
    responses={
        200: {
            "description": "Информация о клиенте успешно получена.",
            "model": ClientResponse,
        },
        400: {
            "description": "Некорректные данные запроса.",
            "model": InvalidRequestResponse,
        },
        404: {"description": "Клиент не найден.", "model": NotFoundResponse},
    },
)
async def get_client(
    client_id: Annotated[UUID4, Path(description="UUID клиента.")],
    client_service: FromDishka[ClientService],
) -> ClientResponse:
    response = await client_service.get_client(client_id)

    return ClientResponse(
        client_id=response.client_id,
        login=response.login,
        age=response.age,
        location=response.location,
        gender=response.gender,
    )


@router.post(
    "/bulk",
    summary="Массовое создание/обновление клиентов",
    description="Создаёт новых или обновляет существующих клиентов",
    status_code=201,
    responses={
        201: {
            "description": "Успешное создание/обновление клиентов",
            "model": list[ClientResponse],
        },
        400: {
            "description": "Некорректные данные запроса.",
            "model": InvalidRequestResponse,
        },
    },
)
async def create_or_update_clients(
    body: list[ClientUpsertRequest],
    client_service: FromDishka[ClientService],
) -> list[ClientResponse]:
    response = await client_service.upsert_clients(body)

    return [
        ClientResponse(
            client_id=client.client_id,
            login=client.login,
            age=client.age,
            location=client.location,
            gender=client.gender,
        )
        for client in response
    ]
