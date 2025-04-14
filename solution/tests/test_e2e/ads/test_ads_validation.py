from typing import Any
from httpx import AsyncClient
import pytest


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "client_id", ["123-123", "3fa85f64-5717-4562-b3fc-2c96366afa6"]
)
async def test_ads_validation(client: AsyncClient, client_id: str):
    response = await client.get("/ads", params={"client_id": client_id})

    assert response.status_code == 400


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "ad_id, client_id",
    [
        ("123-123", "123-123"),
        ("3fa85f64-5717-4562-b3fc-2c963f66afa6", "3fa85f64-5717-452-bfc-2c963f66afa6"),
        ("3fa85f64-5717-4562-b3fc-2c963f66afa6", "123-123"),
    ],
)
async def test_click_validation(client: AsyncClient, ad_id: str, client_id: str):
    response = await client.post(f"/ads/{ad_id}/click", json={"client_id": client_id})

    assert response.status_code == 400
