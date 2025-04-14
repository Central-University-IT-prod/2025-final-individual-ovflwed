from ad_platform.application.services.campaigns import CampaignService
from ad_platform.application.services.stats_service import StatsService
from ad_platform.domain.entities import CampaignId, DailyStats, Stats
from ad_platform.infrastructure.db.commiter import Commiter


class GetCampaignStatsInteractor:
    def __init__(
        self,
        campaign_service: CampaignService,
        stats_service: StatsService,
        commiter: Commiter,
    ) -> None:
        self.campaign_service = campaign_service
        self.stats_service = stats_service
        self.commiter = commiter

    async def __call__(self, campaign_id: CampaignId) -> Stats:
        async with self.commiter:
            await self.campaign_service.ensure_campaign_exists_ever(campaign_id)

            return await self.stats_service.get_campaign_stats(campaign_id)


class GetCampaignDailyStatsInteractor:
    def __init__(
        self,
        campaign_service: CampaignService,
        stats_service: StatsService,
        commiter: Commiter,
    ) -> None:
        self.campaign_service = campaign_service
        self.stats_service = stats_service
        self.commiter = commiter

    async def __call__(self, campaign_id: CampaignId) -> list[DailyStats]:
        async with self.commiter:
            await self.campaign_service.ensure_campaign_exists_ever(campaign_id)

            return await self.stats_service.get_campaign_daily_stats(campaign_id)
