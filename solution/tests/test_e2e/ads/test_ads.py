from typing import Any
from httpx import AsyncClient
import pytest


@pytest.mark.asyncio
async def test_get_ads(
    client: AsyncClient,
    client_data: dict[str, Any],
    created_active_campaign: dict[str, Any],
):
    client_data["age"] = 20

    response = await client.post(f"/clients/bulk", json=[client_data])
    assert response.status_code == 201

    response = await client.get(f"/ads", params={"client_id": client_data["client_id"]})
    assert response.status_code == 200

    assert response.json()["ad_id"] == created_active_campaign["campaign_id"]


@pytest.mark.asyncio
async def test_click_ad(
    client: AsyncClient,
    client_data: dict[str, Any],
    created_active_campaign: dict[str, Any],
):
    client_data["age"] = 20

    response = await client.post(f"/clients/bulk", json=[client_data])
    assert response.status_code == 201

    response = await client.get(f"/ads", params={"client_id": client_data["client_id"]})
    assert response.status_code == 200

    response = await client.post(
        f"/ads/{response.json()['ad_id']}/click",
        json={"client_id": client_data["client_id"]},
    )
    assert response.status_code == 204
