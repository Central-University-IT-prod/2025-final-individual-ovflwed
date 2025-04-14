from typing import Any
from httpx import AsyncClient
import pytest


def get_broken_client_data(field: str, value: Any) -> list:
    data = [
        {
            "age": 40,
            "client_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "gender": "MALE",
            "location": "string",
            "login": "string",
        }
    ]
    data[0][field] = value

    return data


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "client_id, expected_status_code",
    [
        ("3fa85f64-5717-4562-b3fc-2c963f66afa6", 404),
        ("3fa85f6457174562b3fc2c963f66afa6", 404),
        ("123-123", 400),
        ("3fa85f6457174562b3fc2c963f66afa", 400),
    ],
)
async def test_get_client_validation(
    client: AsyncClient, client_id: str, expected_status_code: int
):
    response = await client.get(f"/clients/{client_id}")
    assert response.status_code == expected_status_code


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "data, expected_status_code",
    [
        (get_broken_client_data("client_id", "3fa85f64-5717-45622c963f66afa6"), 400),
        (get_broken_client_data("client_id", "123-123"), 400),
        (get_broken_client_data("age", ""), 400),
        (get_broken_client_data("age", -1), 400),
        (get_broken_client_data("gender", "ALL"), 400),
        (get_broken_client_data("gender", ""), 400),
        (get_broken_client_data("location", ""), 400),
        (get_broken_client_data("login", ""), 400),
    ],
)
async def test_add_client_validation(
    client: AsyncClient, data: list[dict], expected_status_code: int
):
    response = await client.post(f"/clients/bulk", json=data)
    assert response.status_code == expected_status_code
