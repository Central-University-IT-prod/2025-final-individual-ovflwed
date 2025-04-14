import logging
from typing import cast

from asyncpg import Connection

from ad_platform.domain.entities import Advertiser, AdvertiserId
from ad_platform.infrastructure.db.gateways.common import AdvertiserGateway

logger = logging.getLogger(__name__)


class AdvertiserGatewayImpl(AdvertiserGateway):
    def __init__(self, conn: Connection) -> None:
        self.conn = conn

    async def get_advertiser(self, advertiser_id: AdvertiserId) -> Advertiser | None:
        logger.info("Getting advertiser %s", advertiser_id)

        advertiser = await self.conn.fetchrow(
            "SELECT advertiser_id, name FROM advertisers WHERE advertiser_id = $1",
            advertiser_id,
        )

        if not advertiser:
            return None

        return Advertiser(
            advertiser_id=cast(AdvertiserId, advertiser["advertiser_id"]),
            name=advertiser["name"],
        )

    async def upsert_advertisers(self, advertisers: list[Advertiser]) -> None:
        logger.info(
            "Upserting %s advertisers: %s",
            len(advertisers),
            [x.advertiser_id for x in advertisers],
        )

        await self.conn.executemany(
            """
            INSERT INTO advertisers (advertiser_id, name)
            VALUES ($1, $2)
            ON CONFLICT (advertiser_id)
            DO UPDATE SET name = $2;
            """,
            [(client.advertiser_id, client.name) for client in advertisers],
        )
