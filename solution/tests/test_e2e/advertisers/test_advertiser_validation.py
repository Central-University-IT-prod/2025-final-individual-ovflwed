from typing import Any
from httpx import AsyncClient
import pytest


def get_broken_advertiser_data(field: str, value: Any) -> list:
    data = [{"advertiser_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6", "name": "Booo"}]
    data[0][field] = value

    return data


def get_broken_ml_score(field: str, value: Any) -> dict:
    data = {
        "advertiser_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "client_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "score": 0,
    }
    data[field] = value

    return data


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "advertiser_id, expected_status_code",
    [
        ("3fa85f64-5717-4562-b3fc-2c963f66afa6", 404),
        ("3fa85f6457174562b3fc2c963f66afa6", 404),
        ("123-123", 400),
        ("3fa85f6457174562b3fc2c963f66afa", 400),
    ],
)
async def test_get_advertiser_validation(
    client: AsyncClient, advertiser_id: str, expected_status_code: int
):
    response = await client.get(f"/advertisers/{advertiser_id}")
    assert response.status_code == expected_status_code


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "data, expected_status_code",
    [
        (
            get_broken_advertiser_data(
                "advertiser_id", "3fa85f64-5717-45622c963f66afa6"
            ),
            400,
        ),
        (get_broken_advertiser_data("advertiser_id", "123-123"), 400),
        (get_broken_advertiser_data("name", ""), 400),
        (get_broken_advertiser_data("name", -1), 400),
    ],
)
async def test_add_advertiser_validation(
    client: AsyncClient, data: list[dict], expected_status_code: int
):
    response = await client.post(f"/advertisers/bulk", json=data)
    assert response.status_code == expected_status_code


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "data, expected_status_code",
    [
        (get_broken_ml_score("advertiser_id", "3fa85f64-5717-45622c963f66afa6"), 400),
        (get_broken_ml_score("advertiser_id", "123-123"), 400),
        (get_broken_ml_score("client_id", ""), 400),
        (get_broken_ml_score("client_id", -1), 400),
        (get_broken_ml_score("score", ""), 400),
        (get_broken_ml_score("score", -1), 400),
    ],
)
async def test_add_score_validation(
    client: AsyncClient, data: dict, expected_status_code: int
):
    response = await client.post(f"/ml-scores", json=data)
    assert response.status_code == expected_status_code
