from typing import Any
from asyncpg import Connection
from httpx import AsyncClient
import pytest


@pytest.mark.asyncio
async def test_get_campaign_stats(
    client: AsyncClient,
    client_data: dict[str, Any],
    created_active_campaign: dict[str, Any],
    db_connection: Connection,
):
    client_data["age"] = 20

    response = await client.post(f"/clients/bulk", json=[client_data])
    assert response.status_code == 201

    response = await client.get(f"/ads", params={"client_id": client_data["client_id"]})
    assert response.status_code == 200

    ad_id = response.json()["ad_id"]

    response = await client.get(f"/stats/campaigns/{ad_id}")
    assert response.status_code == 200

    assert response.json()["impressions_count"] == 1
    assert response.json()["clicks_count"] == 0

    response = await client.post(
        f"/ads/{ad_id}/click", json={"client_id": client_data["client_id"]}
    )
    assert response.status_code == 204

    response = await client.get(f"/stats/campaigns/{ad_id}")
    assert response.status_code == 200

    assert response.json()["impressions_count"] == 1
    assert response.json()["clicks_count"] == 1

    await db_connection.execute(
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
