from typing import Any
from httpx import AsyncClient
import pytest


def get_broken_campaign_data(field: str, value: Any) -> dict:
    data = {
        "ad_text": "string",
        "ad_title": "string",
        "clicks_limit": 0,
        "cost_per_click": 0,
        "cost_per_impression": 0,
        "end_date": 1,
        "impressions_limit": 0,
        "start_date": 1,
        "targeting": {
            "age_from": 0,
            "age_to": 0,
            "gender": "MALE",
            "location": "string",
        },
    }
    data[field] = value

    return data


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "data, expected_status_code",
    [
        (
            [
                "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            ],
            404,
        ),
        (["3fa85f6457174562b3fc2c963f66afa6", "3fa85f6457174562b3fc2c963f66afa6"], 404),
        (["123-123", "123-123"], 400),
        (["3fa85f6457174562b3fc2c963f66afa", "3fa85f6457174562b3fc2c963f66afa6"], 400),
    ],
)
async def test_get_campaign_validation(
    client: AsyncClient, data: list[str], expected_status_code: int
):
    response = await client.get(f"/advertisers/{data[0]}/campaigns/{data[1]}")
    assert response.status_code == expected_status_code


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "data, expected_status_code",
    [
        (["123-123", "123-123"], 400),
        (["3fa85f6457174562b3fc2c963f66afa", "3fa85f6457174562b3fc2c963f66afa6"], 400),
    ],
)
async def test_put_campaign_validation(
    client: AsyncClient, data: list[str], expected_status_code: int
):
    response = await client.put(f"/advertisers/{data[0]}/campaigns/{data[1]}")
    assert response.status_code == expected_status_code


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "data, expected_status_code",
    [
        (
            [
                "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            ],
            404,
        ),
        (["3fa85f6457174562b3fc2c963f66afa6", "3fa85f6457174562b3fc2c963f66afa6"], 404),
        (["123-123", "123-123"], 400),
        (["3fa85f6457174562b3fc2c963f66afa", "3fa85f6457174562b3fc2c963f66afa6"], 400),
    ],
)
async def test_delete_campaign_validation(
    client: AsyncClient, data: list[str], expected_status_code: int
):
    response = await client.delete(f"/advertisers/{data[0]}/campaigns/{data[1]}")
    assert response.status_code == expected_status_code


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "data, expected_status_code",
    [
        (get_broken_campaign_data("ad_text", ""), 400),
        (get_broken_campaign_data("ad_text", -1), 400),
        (get_broken_campaign_data("ad_title", ""), 400),
        (get_broken_campaign_data("ad_title", -1), 400),
        (get_broken_campaign_data("clicks_limit", ""), 400),
        (get_broken_campaign_data("clicks_limit", -1), 400),
        (get_broken_campaign_data("cost_per_click", ""), 400),
        (get_broken_campaign_data("cost_per_click", -1), 400),
        (get_broken_campaign_data("cost_per_impression", ""), 400),
        (get_broken_campaign_data("cost_per_impression", -1), 400),
        (get_broken_campaign_data("end_date", ""), 400),
        (get_broken_campaign_data("end_date", -1), 400),
        (get_broken_campaign_data("impressions_limit", ""), 400),
        (get_broken_campaign_data("impressions_limit", -1), 400),
        (get_broken_campaign_data("start_date", ""), 400),
        (get_broken_campaign_data("start_date", -1), 400),
    ],
)
async def test_create_campaign_validation(
    client: AsyncClient,
    data: dict,
    expected_status_code: int,
    created_advertiser: dict[str, Any],
):
    print(data)
    response = await client.post(
        "/advertisers/3fa85f64-5717-4562-b3fc-2c963f66afa6/campaigns", json=data
    )
    assert response.status_code == expected_status_code


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "advertiser_id, expected_status_code",
    [
        ("123-123", 400),
        ("3fa85f6457174562b3fc2c963f66afa", 400),
    ],
)
async def test_get_paginated_campaign_validation(
    client: AsyncClient, advertiser_id: str, expected_status_code: int
):
    response = await client.get(f"/advertisers/{advertiser_id}/campaigns")
    assert response.status_code == expected_status_code


@pytest.mark.asyncio
async def test_add_image_campaign_validation(
    client: AsyncClient, created_campaign: dict[str, Any]
):
    response = await client.post(
        f"/advertisers/{created_campaign['advertiser_id']}/campaigns/{created_campaign['id']}/images"
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_add_image_campaign_validation(
    client: AsyncClient, created_campaign: dict[str, Any], file
):
    response = await client.post(
        f"/advertisers/{created_campaign['advertiser_id']}/campaigns/{created_campaign['campaign_id']}/image",
        files={"file": file},
    )
    assert response.status_code == 400


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "data, expected_status_code",
    [
        (
            [
                "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            ],
            404,
        ),
        (["3fa85f6457174562b3fc2c963f66afa6", "3fa85f6457174562b3fc2c963f66afa6"], 404),
        (["123-123", "123-123"], 400),
        (["3fa85f6457174562b3fc2c963f66afa", "3fa85f6457174562b3fc2c963f66afa6"], 400),
    ],
)
async def test_delete_image_campaign_validation(
    client: AsyncClient, data: list[str], expected_status_code: int
):
    response = await client.delete(f"/advertisers/{data[0]}/campaigns/{data[1]}/image")
    assert response.status_code == expected_status_code
