from ad_platform.domain.entities import AdvertiserId, CampaignId, DailyStats, Stats
from ad_platform.infrastructure.db.gateways.common import ActionsGateway


class StatsService:
    def __init__(
        self,
        action_gateway: ActionsGateway,
    ) -> None:
        self.action_gateway = action_gateway

    async def get_campaign_stats(self, campaign_id: CampaignId) -> Stats:
        res = await self.action_gateway.get_campaign_stats(campaign_id)

        res.conversion = (
            res.clicks_count / res.impressions_count
            if res.impressions_count != 0
            else 0
        )

        return res

    async def get_advertiser_stats(self, advertiser_id: AdvertiserId) -> Stats:
        res = await self.action_gateway.get_advertiser_stats(advertiser_id)

        res.conversion = (
            res.clicks_count / res.impressions_count
            if res.impressions_count != 0
            else 0
        )

        return res

    async def get_campaign_daily_stats(
        self,
        campaign_id: CampaignId,
    ) -> list[DailyStats]:
        res = await self.action_gateway.get_campaign_daily_stats(
            campaign_id,
        )

        for day in res:
            day.conversion = (
                day.clicks_count / day.impressions_count
                if day.impressions_count != 0
                else 0
            )

        return res

    async def get_advertiser_daily_stats(
        self,
        advertiser_id: AdvertiserId,
    ) -> list[DailyStats]:
        res = await self.action_gateway.get_advertiser_daily_stats(
            advertiser_id,
        )

        for day in res:
            day.conversion = (
                day.clicks_count / day.impressions_count
                if day.impressions_count != 0
                else 0
            )

        return res
