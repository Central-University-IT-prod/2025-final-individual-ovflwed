from typing import Any
from asyncpg import Connection
from httpx import AsyncClient
import pytest


@pytest.mark.asyncio
async def test_create_campaign(
    client: AsyncClient,
    created_advertiser: dict[str, Any],
    db_connection: Connection,
    campaign_data: dict[str, Any],
):
    response = await client.post(
        f"/advertisers/{created_advertiser['advertiser_id']}/campaigns",
        json=campaign_data,
    )
    assert response.status_code == 201

    db_campaign = await db_connection.fetchrow(
        "SELECT * FROM campaigns WHERE campaign_id = $1", response.json()["campaign_id"]
    )

    assert str(db_campaign["campaign_id"]) == response.json()["campaign_id"]
    assert str(db_campaign["advertiser_id"]) == created_advertiser["advertiser_id"]
    assert db_campaign["ad_text"] == campaign_data["ad_text"]
    assert db_campaign["ad_title"] == campaign_data["ad_title"]
    assert db_campaign["start_date"] == campaign_data["start_date"]
    assert db_campaign["end_date"] == campaign_data["end_date"]
    assert db_campaign["impressions_limit"] == campaign_data["impressions_limit"]
    assert db_campaign["clicks_limit"] == campaign_data["clicks_limit"]
    assert db_campaign["cost_per_impression"] == campaign_data["cost_per_impression"]
    assert db_campaign["cost_per_click"] == campaign_data["cost_per_click"]
    assert db_campaign["image_url"] == None
    assert db_campaign["age_from"] == campaign_data["targeting"].get("age_from")
    assert db_campaign["age_to"] == campaign_data["targeting"].get("age_to")
    assert db_campaign["gender"] == campaign_data["targeting"].get("gender")
    assert db_campaign["loc"] == campaign_data["targeting"].get("location")

    response = await client.get(
        f"/advertisers/{created_advertiser['advertiser_id']}/campaigns"
    )

    assert response.status_code == 200
    assert len(response.json()) == 1

    response = await client.get(
        f"/advertisers/{created_advertiser['advertiser_id']}/campaigns/{response.json()[0]['campaign_id']}"
    )

    assert response.status_code == 200
    assert response.json()["advertiser_id"] == created_advertiser["advertiser_id"]


@pytest.mark.asyncio
async def test_update_campaign(
    client: AsyncClient, created_campaign: dict[str, Any], campaign_data: dict[str, Any]
):
    created_campaign["ad_text"] = "New Ad Text"

    response = await client.put(
        f"/advertisers/{created_campaign['advertiser_id']}/campaigns/{created_campaign['campaign_id']}",
        json=created_campaign,
    )

    print(response.json())
    assert response.status_code == 200

    response = await client.get(
        f"/advertisers/{created_campaign['advertiser_id']}/campaigns/{created_campaign['campaign_id']}"
    )

    assert response.status_code == 200
    assert response.json()["ad_text"] == "New Ad Text"


@pytest.mark.asyncio
async def test_delete_campaign(
    client: AsyncClient,
    created_campaign: dict[str, Any],
    created_advertiser: dict[str, Any],
):
    response = await client.delete(
        f"/advertisers/{created_advertiser['advertiser_id']}/campaigns/{created_campaign['campaign_id']}"
    )

    assert response.status_code == 204

    response = await client.get(
        f"/advertisers/{created_advertiser['advertiser_id']}/campaigns/{created_campaign['campaign_id']}"
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_add_image_invalid_campaign(
    client: AsyncClient,
    created_campaign: dict[str, Any],
    created_advertiser: dict[str, Any],
    file,
):
    response = await client.post(
        f"/advertisers/{created_advertiser['advertiser_id']}/campaigns/{created_campaign['campaign_id']}/image",
        files={"file": file},
    )

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_add_image_campaign(
    client: AsyncClient,
    created_campaign: dict[str, Any],
    created_advertiser: dict[str, Any],
    file_valid,
):
    response = await client.post(
        f"/advertisers/{created_advertiser['advertiser_id']}/campaigns/{created_campaign['campaign_id']}/image",
        files={"file": file_valid},
    )

    print(response.json())
    assert response.status_code == 200

    response = await client.get(
        f"/advertisers/{created_advertiser['advertiser_id']}/campaigns/{created_campaign['campaign_id']}"
    )

    assert response.status_code == 200
    assert response.json()["image_url"]

    response = await client.get(response.json()["image_url"])

    assert response.status_code == 200

    response = await client.delete(
        f"/advertisers/{created_advertiser['advertiser_id']}/campaigns/{created_campaign['campaign_id']}/image"
    )

    assert response.status_code == 204

    response = await client.get(
        f"/advertisers/{created_advertiser['advertiser_id']}/campaigns/{created_campaign['campaign_id']}"
    )

    assert response.status_code == 200
    assert response.json()["image_url"] is None
