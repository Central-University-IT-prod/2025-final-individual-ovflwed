import logging

from asyncpg import Connection

from ad_platform.domain.entities import Score
from ad_platform.infrastructure.db.gateways.common import ScoresGateway

logger = logging.getLogger(__name__)


class ScoresGatewayImpl(ScoresGateway):
    def __init__(self, conn: Connection) -> None:
        self.conn = conn

    async def upsert_score(self, score: Score) -> None:
        logger.info("Upserting score %s", score)

        await self.conn.execute(
            """
            INSERT INTO scores (client_id, advertiser_id, score)
            VALUES ($1, $2, $3)
            ON CONFLICT (client_id, advertiser_id)
            DO UPDATE SET score = $3;
            """,
            score.client_id,
            score.advertiser_id,
            score.score,
        )
