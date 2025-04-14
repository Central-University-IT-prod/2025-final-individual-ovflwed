import logging

from asyncpg import Connection

from ad_platform.domain.entities import (
    AdvertiserId,
    Campaign,
    CampaignId,
    CampaignTarget,
    ClientId,
    Gender,
)
from ad_platform.infrastructure.db.gateways.common import CampaignGateway

logger = logging.getLogger(__name__)


class CampaignGatewayImpl(CampaignGateway):
    def __init__(self, conn: Connection) -> None:
        self.conn = conn

    async def create_campaign(self, campaign: Campaign) -> None:
        await self.conn.execute(
            """
            INSERT INTO campaigns (
                campaign_id,
                advertiser_id,
                ad_title,
                ad_text,
                start_date,
                end_date,
                impressions_limit,
                clicks_limit,
                cost_per_impression,
                cost_per_click,
                age_from,
                age_to,
                gender,
                loc
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14);
        """,
            campaign.campaign_id,
            campaign.advertiser_id,
            campaign.ad_title,
            campaign.ad_text,
            campaign.start_date,
            campaign.end_date,
            campaign.impressions_limit,
            campaign.clicks_limit,
            campaign.cost_per_impression,
            campaign.cost_per_click,
            campaign.targeting.age_from,
            campaign.targeting.age_to,
            campaign.targeting.gender.value if campaign.targeting.gender else None,
            campaign.targeting.location,
        )

    async def update_campaign(self, campaign: Campaign) -> None:
        await self.conn.execute(
            """
            UPDATE active_campaigns
            SET
                ad_title = $2,
                ad_text = $3,
                start_date = $4,
                end_date = $5,
                impressions_limit = $6,
                clicks_limit = $7,
                cost_per_impression = $8,
                cost_per_click = $9,
                age_from = $10,
                age_to = $11,
                gender = $12,
                loc = $13
            WHERE campaign_id = $1;
        """,
            campaign.campaign_id,
            campaign.ad_title,
            campaign.ad_text,
            campaign.start_date,
            campaign.end_date,
            campaign.impressions_limit,
            campaign.clicks_limit,
            campaign.cost_per_impression,
            campaign.cost_per_click,
            campaign.targeting.age_from,
            campaign.targeting.age_to,
            campaign.targeting.gender.value if campaign.targeting.gender else None,
            campaign.targeting.location,
        )

    async def delete_campaign(
        self,
        campaign_id: CampaignId,
    ) -> None:
        await self.conn.execute(
            "UPDATE campaigns SET is_deleted = TRUE WHERE campaign_id = $1",
            campaign_id,
        )

    async def get_campaign(self, campaign_id: CampaignId) -> Campaign | None:
        res = await self.conn.fetchrow(
            "SELECT * FROM active_campaigns WHERE campaign_id = $1;",
            campaign_id,
        )

        if res is None:
            return None

        return Campaign(
            campaign_id=res["campaign_id"],
            advertiser_id=res["advertiser_id"],
            ad_title=res["ad_title"],
            ad_text=res["ad_text"],
            start_date=res["start_date"],
            end_date=res["end_date"],
            impressions_limit=res["impressions_limit"],
            clicks_limit=res["clicks_limit"],
            cost_per_impression=res["cost_per_impression"],
            cost_per_click=res["cost_per_click"],
            image_url=res["image_url"],
            targeting=CampaignTarget(
                age_from=res["age_from"],
                age_to=res["age_to"],
                gender=Gender[res["gender"]] if res["gender"] else None,
                location=res["loc"],
            ),
        )

    async def get_campaign_deleted(self, campaign_id: CampaignId) -> Campaign | None:
        res = await self.conn.fetchrow(
            "SELECT * FROM campaigns WHERE campaign_id = $1;",
            campaign_id,
        )

        if res is None:
            return None

        return Campaign(
            campaign_id=res["campaign_id"],
            advertiser_id=res["advertiser_id"],
            ad_title=res["ad_title"],
            ad_text=res["ad_text"],
            start_date=res["start_date"],
            end_date=res["end_date"],
            impressions_limit=res["impressions_limit"],
            clicks_limit=res["clicks_limit"],
            cost_per_impression=res["cost_per_impression"],
            cost_per_click=res["cost_per_click"],
            image_url=res["image_url"],
            targeting=CampaignTarget(
                age_from=res["age_from"],
                age_to=res["age_to"],
                gender=Gender[res["gender"]] if res["gender"] else None,
                location=res["loc"],
            ),
        )

    async def get_campaigns(
        self,
        advertiser_id: AdvertiserId,
        page: int,
        size: int,
    ) -> list[Campaign]:
        logger.info("get_campaigns %s %s %s", advertiser_id, page, size)
        res = await self.conn.fetch(
            "SELECT * FROM active_campaigns WHERE advertiser_id = $1 LIMIT $2 OFFSET $3;",
            advertiser_id,
            size,
            page * size,
        )

        return [
            Campaign(
                campaign_id=r["campaign_id"],
                advertiser_id=r["advertiser_id"],
                ad_title=r["ad_title"],
                ad_text=r["ad_text"],
                start_date=r["start_date"],
                end_date=r["end_date"],
                impressions_limit=r["impressions_limit"],
                clicks_limit=r["clicks_limit"],
                cost_per_impression=r["cost_per_impression"],
                cost_per_click=r["cost_per_click"],
                image_url=r["image_url"],
                targeting=CampaignTarget(
                    age_from=r["age_from"],
                    age_to=r["age_to"],
                    gender=Gender[r["gender"]] if r["gender"] else None,
                    location=r["loc"],
                ),
            )
            for r in res
        ]

    async def get_target_campaign(
        self,
        day: int,
        gender: Gender,
        age: int,
        location: str,
        client_id: ClientId,
    ) -> Campaign | None:
        logger.info("get_target_campaign %s %s %s %s", day, gender, age, location)
        res = await self.conn.fetchrow(
            """
            WITH campaign_scores AS (
                SELECT c.*,
                    COALESCE(s.score, 0) AS score,
                    (COALESCE(s.score, 0) / (SELECT MAX(score)
                        FROM scores WHERE advertiser_id = c.advertiser_id))
                    AS normalized_score,
                    (COALESCE(c.cost_per_impression, 0) /
                        (SELECT MAX(cost_per_impression)
                            FROM active_campaigns WHERE cost_per_impression IS NOT NULL))
                        AS normalized_price_per_impression,
                    (COALESCE(c.cost_per_click, 0) /
                        (SELECT MAX(cost_per_click)
                            FROM active_campaigns WHERE cost_per_click IS NOT NULL))
                        AS normalized_price_per_click
                FROM active_campaigns c
                LEFT JOIN scores s ON c.advertiser_id = s.advertiser_id
                    AND (s.client_id = $5)
                WHERE c.end_date >= $1
                    AND c.start_date <= $1
                    AND (c.gender = 'ALL' OR c.gender = $2)
                    AND (c.age_from IS NULL OR c.age_from <= $3)
                    AND (c.age_to IS NULL OR c.age_to >= $3)
                    AND (c.loc IS NULL OR c.loc = $4)
            ), ic AS (
                SELECT
                    campaign_id,
                    COALESCE(COUNT(*), 0) AS impression_count
                FROM
                    impressions
                WHERE
                    campaign_id IN (SELECT campaign_id FROM campaign_scores)
                GROUP BY
                    campaign_id
            ), cc AS (
                SELECT
                    campaign_id,
                    COALESCE(COUNT(*), 0) AS click_count
                FROM
                    clicks
                WHERE
                    campaign_id IN (SELECT campaign_id FROM campaign_scores)
                GROUP BY
                    campaign_id
            )
            SELECT
                cs.*,
                COALESCE(impression_count, 0) AS impressions,
                COALESCE(click_count, 0) AS clicks
            FROM
                campaign_scores cs
            LEFT JOIN
                ic  ON cs.campaign_id = ic.campaign_id
            LEFT JOIN
                cc ON cs.campaign_id = cc.campaign_id
            WHERE
                (cs.impressions_limit * 1.05) > COALESCE(impression_count, 0)
                AND (cs.clicks_limit) >= COALESCE(click_count, 0)
                AND (SELECT count(*) FROM clicks WHERE client_id = $5
                    AND campaign_id = cs.campaign_id) = 0
            ORDER BY
                (
                    2 * (cs.normalized_price_per_impression + 0.2 * cs.normalized_price_per_click)
                    + 1.5 * cs.normalized_score
                ) DESC
            LIMIT 1
            """,
            day,
            gender.value,
            age,
            location,
            client_id,
        )

        logger.info("get_target_campaign %s", res)

        if res is None:
            return None

        return Campaign(
            campaign_id=res["campaign_id"],
            advertiser_id=res["advertiser_id"],
            ad_title=res["ad_title"],
            ad_text=res["ad_text"],
            start_date=res["start_date"],
            end_date=res["end_date"],
            impressions_limit=res["impressions_limit"],
            clicks_limit=res["clicks_limit"],
            cost_per_impression=res["cost_per_impression"],
            cost_per_click=res["cost_per_click"],
            image_url=res["image_url"],
            targeting=CampaignTarget(
                age_from=res["age_from"],
                age_to=res["age_to"],
                gender=Gender[res["gender"]] if res["gender"] else None,
                location=res["loc"],
            ),
        )

    async def update_campaign_image(
        self,
        campaign_id: CampaignId,
        image_url: str,
    ) -> None:
        await self.conn.execute(
            "UPDATE active_campaigns SET image_url = $1 WHERE campaign_id = $2",
            image_url,
            campaign_id,
        )
