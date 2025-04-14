from typing import Any
from asyncpg import Connection
from httpx import AsyncClient
import pytest


@pytest.mark.asyncio
async def test_add_client(
    client: AsyncClient, client_data: dict[str, Any], db_connection: Connection
):
    response = await client.post(f"/clients/bulk", json=[client_data])
    assert response.status_code == 201
    assert response.json() == [client_data]

    db_client = await db_connection.fetchrow(
        "SELECT * FROM clients WHERE client_id = $1", client_data["client_id"]
    )

    assert str(db_client["client_id"]) == client_data["client_id"]
    assert db_client["age"] == client_data["age"]
    assert db_client["gender"] == client_data["gender"]
    assert db_client["loc"] == client_data["location"]
    assert db_client["login"] == client_data["login"]


@pytest.mark.asyncio
async def test_update_client(
    client: AsyncClient, created_client: dict[str, Any], db_connection: Connection
):
    created_client["location"] = "New York"

    response = await client.post(f"/clients/bulk", json=[created_client])
    assert response.status_code == 201
    assert response.json() == [created_client]

    db_client = await db_connection.fetchrow(
        "SELECT * FROM clients WHERE client_id = $1", created_client["client_id"]
    )

    assert str(db_client["client_id"]) == created_client["client_id"]
    assert db_client["age"] == created_client["age"]
    assert db_client["gender"] == created_client["gender"]
    assert db_client["loc"] == created_client["location"]
    assert db_client["login"] == created_client["login"]


@pytest.mark.asyncio
async def test_get_client(client: AsyncClient, created_client: dict[str, Any]):
    response = await client.get(f"/clients/{created_client['client_id']}")

    assert response.status_code == 200
    assert response.json() == created_client
