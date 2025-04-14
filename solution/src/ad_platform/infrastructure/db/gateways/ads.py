from asyncpg import Connection, Record

from ad_platform.domain.entities import (
    AdvertiserId,
    CampaignId,
    Click,
    DailyStats,
    Impression,
    Stats,
)
from ad_platform.infrastructure.db.gateways.common import ActionsGateway


class ActionsGatewayImpl(ActionsGateway):
    def __init__(self, conn: Connection) -> None:
        self.conn = conn

    def combine_stats(
        self,
        cliks: list[Record],
        imps: list[Record],
    ) -> list[DailyStats]:
        combined_data = {}

        for day in imps:
            combined_data[day["day"]] = {
                "impressions_cost": day["impressions_cost"],
                "impressions_total": day["impressions_total"],
                "clicks_cost": 0,
                "clicks_total": 0,
            }

        for day in cliks:
            if day["day"] in combined_data:
                combined_data[day["day"]]["clicks_cost"] = day["clicks_cost"]
                combined_data[day["day"]]["clicks_total"] = day["clicks_total"]
            else:
                combined_data[day["day"]] = {
                    "impressions_cost": 0,
                    "impressions_total": 0,
                    "clicks_cost": day["clicks_cost"],
                    "clicks_total": day["clicks_total"],
                }

        resp = []
        for day, data in combined_data.items():
            resp.append(
                DailyStats(
                    clicks_count=data["clicks_total"],
                    spent_clicks=data["clicks_cost"],
                    impressions_count=data["impressions_total"],
                    spent_impressions=data["impressions_cost"],
                    date=day,
                    conversion=0,
                    spent_total=data["clicks_cost"] + data["impressions_cost"],
                ),
            )

        return resp

    async def create_impression(self, impression: Impression) -> None:
        await self.conn.execute(
            """
            INSERT INTO impressions (campaign_id, client_id, day, price) VALUES ($1, $2, $3, $4)
            ON CONFLICT DO NOTHING
            """,
            impression.campaign_id,
            impression.client_id,
            impression.day,
            impression.price,
        )

    async def create_click(self, click: Click) -> None:
        await self.conn.execute(
            """
            INSERT INTO clicks (campaign_id, client_id, day, price) VALUES ($1, $2, $3, $4)
            ON CONFLICT DO NOTHING
            """,
            click.campaign_id,
            click.client_id,
            click.day,
            click.price,
        )

    async def get_impression(
        self,
        campaign_id: str,
        client_id: str,
    ) -> Impression | None:
        res = await self.conn.fetchrow(
            "SELECT day, price FROM impressions WHERE campaign_id = $1 AND client_id = $2",
            campaign_id,
            client_id,
        )

        if res is None:
            return None

        return Impression(
            campaign_id=campaign_id,
            client_id=client_id,
            day=res["day"],
            price=res["price"],
        )

    async def get_click(self, campaign_id: str, client_id: str) -> Click | None:
        res = await self.conn.fetchrow(
            "SELECT day, price FROM clicks WHERE campaign_id = $1 AND client_id = $2",
            campaign_id,
            client_id,
        )

        if res is None:
            return None

        return Click(
            campaign_id=campaign_id,
            client_id=client_id,
            day=res["day"],
            price=res["price"],
        )

    async def get_campaign_stats(self, campaign_id: CampaignId) -> Stats:
        clicks = await self.conn.fetchrow(
            """SELECT
                SUM(c.price) AS clicks_cost,
                COUNT(c.price) AS total_clicks
            FROM (
                SELECT DISTINCT ON (client_id, campaign_id) price
                FROM clicks c
                WHERE campaign_id = $1
                ORDER BY client_id, campaign_id, serial_id
            ) AS c;""",
            campaign_id,
        )
        if clicks is None:
            clicks = {"clicks_cost": 0, "total_clicks": 0}

        impressions = await self.conn.fetchrow(
            """SELECT
                SUM(i.price) AS impressions_cost,
                COUNT(i.price) AS total_impressions
            FROM (
                SELECT DISTINCT ON (client_id, campaign_id) price
                FROM impressions i
                WHERE campaign_id = $1
                ORDER BY client_id, campaign_id, serial_id
            ) AS i;""",
            campaign_id,
        )
        if impressions is None:
            impressions = {"impressions_cost": 0, "total_impressions": 0}

        resp = Stats(
            impressions_count=impressions["total_impressions"] or 0,
            clicks_count=clicks["total_clicks"] or 0,
            spent_impressions=impressions["impressions_cost"] or 0,
            spent_clicks=clicks["clicks_cost"] or 0,
            conversion=0,
            spent_total=0,
        )

        resp.spent_total = resp.spent_clicks + resp.spent_impressions

        return resp

    async def get_advertiser_stats(self, advertiser_id: AdvertiserId) -> Stats:
        clicks = await self.conn.fetchrow(
            """SELECT
                SUM(c.price) AS clicks_cost,
                COUNT(c.price) AS total_clicks
            FROM (
                SELECT DISTINCT ON (client_id, campaign_id) price, campaign_id
                FROM clicks c
                ORDER BY client_id, campaign_id, serial_id
            ) AS c
            JOIN campaigns cp
                ON c.campaign_id = cp.campaign_id
            WHERE cp.advertiser_id = $1;
            """,
            advertiser_id,
        )

        impressions = await self.conn.fetchrow(
            """SELECT
                SUM(i.price) AS imps_cost,
                COUNT(i.price) AS total_imps
            FROM (
                SELECT DISTINCT ON (client_id, campaign_id) price, campaign_id
                FROM impressions i
                ORDER BY client_id, campaign_id, serial_id
            ) AS i
            JOIN campaigns cp
                ON i.campaign_id = cp.campaign_id
            WHERE cp.advertiser_id = $1;
            """,
            advertiser_id,
        )

        resp = Stats(
            clicks_count=clicks["total_clicks"],
            spent_clicks=clicks["clicks_cost"],
            impressions_count=impressions["total_imps"],
            spent_impressions=impressions["imps_cost"],
            conversion=0,
            spent_total=0,
        )

        resp.spent_total = resp.spent_clicks + resp.spent_impressions

        return resp

    async def get_campaign_daily_stats(
        self,
        campaign_id: CampaignId,
    ) -> list[DailyStats]:
        impressions_res = await self.conn.fetch(
            """SELECT
                COALESCE(SUM(price), 0) AS impressions_cost,
                COALESCE(COUNT(price), 0) AS impressions_total,
                COALESCE(day) AS day
            FROM (
                SELECT DISTINCT ON (client_id, campaign_id) price, day
                FROM impressions
                WHERE campaign_id = $1
                ORDER BY client_id, campaign_id, day, serial_id
            ) AS i
            GROUP BY day
            ORDER BY day;""",
            campaign_id,
        )
        clicks_res = await self.conn.fetch(
            """SELECT
                COALESCE(SUM(price), 0) AS clicks_cost,
                COALESCE(COUNT(price), 0) AS clicks_total,
                COALESCE(day) AS day
            FROM (
                SELECT DISTINCT ON (client_id, campaign_id) price, day
                FROM clicks
                WHERE campaign_id = $1
                ORDER BY client_id, campaign_id, day, serial_id
            ) AS c
            GROUP BY day
            ORDER BY day;""",
            campaign_id,
        )

        return self.combine_stats(clicks_res, impressions_res)

    async def get_advertiser_daily_stats(
        self,
        advertiser_id: AdvertiserId,
    ) -> list[DailyStats]:
        impressions_res = await self.conn.fetch(
            """SELECT
                COALESCE(SUM(price), 0) AS impressions_cost,
                COALESCE(COUNT(price), 0) AS impressions_total,
                COALESCE(day) AS day
            FROM (
                SELECT DISTINCT ON (client_id, campaign_id) price, day, campaign_id
                FROM impressions
                WHERE campaign_id IN (SELECT campaign_id FROM campaigns WHERE advertiser_id = $1)
                ORDER BY client_id, campaign_id, day, serial_id
            ) AS i
            GROUP BY day
            ORDER BY day;""",
            advertiser_id,
        )
        clicks_res = await self.conn.fetch(
            """SELECT
                COALESCE(SUM(price), 0) AS clicks_cost,
                COALESCE(COUNT(price), 0) AS clicks_total,
                COALESCE(day) AS day
            FROM (
                SELECT DISTINCT ON (client_id, campaign_id) price, day, campaign_id
                FROM clicks
                WHERE campaign_id IN (SELECT campaign_id FROM campaigns WHERE advertiser_id = $1)
                ORDER BY client_id, campaign_id, day, serial_id
            ) AS c
            GROUP BY day
            ORDER BY day;""",
            advertiser_id,
        )

        return self.combine_stats(clicks_res, impressions_res)
