import os
from pathlib import Path
from random import randint
from typing import Any
from uuid import uuid4

import asyncpg
import httpx
import pytest
import pytest_asyncio


@pytest_asyncio.fixture
async def client():
    async with httpx.AsyncClient(base_url="http://localhost:8080") as client:
        yield client

    await client.aclose()


@pytest_asyncio.fixture()
async def db_connection():
    conn = await asyncpg.connect(dsn=os.environ["DATABASE_DSN"])

    yield conn

    await conn.execute(
        """DO $$ 
        DECLARE
            r RECORD;
        BEGIN
            FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public' AND tablename <> 'migrations')
            LOOP
                EXECUTE 'TRUNCATE TABLE public.' || r.tablename || ' CASCADE';
            END LOOP;
        END $$;""",
    )

    await conn.close()


@pytest.fixture
def client_data() -> dict[str, Any]:
    return {
        "client_id": str(uuid4()),
        "age": randint(1, 100),
        "gender": "MALE",
        "location": "Moscow",
        "login": "login",
    }


@pytest_asyncio.fixture
async def created_client(
    client: httpx.AsyncClient, client_data: dict[str, Any]
) -> dict[str, Any]:
    response = await client.post(f"/clients/bulk", json=[client_data])
    assert response.status_code == 201
    assert response.json() == [client_data]

    return client_data


@pytest.fixture
def advertiser_data() -> dict[str, Any]:
    return {"advertiser_id": str(uuid4()), "name": "name"}


@pytest_asyncio.fixture
async def created_advertiser(
    client: httpx.AsyncClient, advertiser_data: dict[str, Any]
) -> dict[str, Any]:
    response = await client.post(f"/advertisers/bulk", json=[advertiser_data])
    assert response.status_code == 201
    assert response.json() == [advertiser_data]

    return advertiser_data


@pytest.fixture
def campaign_data() -> dict[str, Any]:
    return {
        "ad_text": "string",
        "ad_title": "string",
        "clicks_limit": 11,
        "cost_per_click": 111,
        "cost_per_impression": 10,
        "end_date": 1,
        "impressions_limit": 2,
        "start_date": 1,
        "targeting": {
            "age_from": 0,
            "age_to": 100,
            "gender": "MALE",
        },
    }


@pytest_asyncio.fixture
async def created_campaign(
    client: httpx.AsyncClient,
    campaign_data: dict[str, Any],
    created_advertiser: dict[str, Any],
) -> dict[str, Any]:
    response = await client.post(
        f"/advertisers/{created_advertiser['advertiser_id']}/campaigns",
        json=campaign_data,
    )
    assert response.status_code == 201

    return response.json()


@pytest_asyncio.fixture
async def created_active_campaign(
    client: httpx.AsyncClient,
    campaign_data: dict[str, Any],
    created_advertiser: dict[str, Any],
) -> dict[str, Any]:
    campaign_data["start_date"] = 0
    response = await client.post(
        f"/advertisers/{created_advertiser['advertiser_id']}/campaigns",
        json=campaign_data,
    )
    assert response.status_code == 201

    return response.json()


@pytest_asyncio.fixture
async def file():
    with (Path(__file__).parent / "files" / "invalid.png").open("rb") as f:
        yield f


@pytest_asyncio.fixture
async def file_valid():
    with (Path(__file__).parent / "files" / "valid.jpg").open("rb") as f:
        yield f
