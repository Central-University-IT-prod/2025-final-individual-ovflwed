from typing import Any
from uuid import uuid4
from asyncpg import Connection
from httpx import AsyncClient
import pytest


@pytest.mark.asyncio
async def test_add_advertiser(
    client: AsyncClient, advertiser_data: dict[str, Any], db_connection: Connection
):
    response = await client.post(f"/advertisers/bulk", json=[advertiser_data])
    assert response.status_code == 201
    assert response.json() == [advertiser_data]

    db_client = await db_connection.fetchrow(
        "SELECT * FROM advertisers WHERE advertiser_id = $1",
        advertiser_data["advertiser_id"],
    )

    assert str(db_client["advertiser_id"]) == advertiser_data["advertiser_id"]
    assert db_client["name"] == advertiser_data["name"]


@pytest.mark.asyncio
async def test_update_advertiser(
    client: AsyncClient, created_advertiser: dict[str, Any], db_connection: Connection
):
    created_advertiser["name"] = "New Name"

    response = await client.post(f"/advertisers/bulk", json=[created_advertiser])
    assert response.status_code == 201
    assert response.json() == [created_advertiser]

    db_client = await db_connection.fetchrow(
        "SELECT * FROM advertisers WHERE advertiser_id = $1",
        created_advertiser["advertiser_id"],
    )

    assert str(db_client["advertiser_id"]) == created_advertiser["advertiser_id"]
    assert db_client["name"] == created_advertiser["name"]


@pytest.mark.asyncio
async def test_get_advertiser(client: AsyncClient, created_advertiser: dict[str, Any]):
    response = await client.get(f"/advertisers/{created_advertiser['advertiser_id']}")

    assert response.status_code == 200
    assert response.json() == created_advertiser


@pytest.mark.asyncio
async def test_get_advertiser(client: AsyncClient, created_advertiser: dict[str, Any]):
    response = await client.get(f"/advertisers/{created_advertiser['advertiser_id']}")

    assert response.status_code == 200
    assert response.json() == created_advertiser


@pytest.mark.asyncio
async def test_add_score(
    client: AsyncClient,
    created_advertiser: dict[str, Any],
    created_client: dict[str, Any],
    db_connection: Connection,
):
    data = {
        "advertiser_id": created_advertiser["advertiser_id"],
        "client_id": created_client["client_id"],
        "score": 5,
    }
    response = await client.post(f"/ml-scores", json=data)

    assert response.status_code == 200

    db_score = await db_connection.fetchrow(
        "SELECT * FROM scores WHERE advertiser_id = $1 AND client_id = $2",
        data["advertiser_id"],
        data["client_id"],
    )

    assert str(db_score["advertiser_id"]) == data["advertiser_id"]
    assert str(db_score["client_id"]) == data["client_id"]
    assert db_score["score"] == data["score"]


@pytest.mark.asyncio
async def test_add_score_no_advertiser(
    client: AsyncClient,
    created_client: dict[str, Any],
    db_connection: Connection,
):
    data = {
        "advertiser_id": str(uuid4()),
        "client_id": created_client["client_id"],
        "score": 5,
    }
    response = await client.post(f"/ml-scores", json=data)

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_add_score_no_client(
    client: AsyncClient,
    created_client: dict[str, Any],
    created_advertiser: dict[str, Any],
    db_connection: Connection,
):
    data = {
        "advertiser_id": created_advertiser["advertiser_id"],
        "client_id": str(uuid4()),
        "score": 5,
    }
    response = await client.post(f"/ml-scores", json=data)

    assert response.status_code == 404
