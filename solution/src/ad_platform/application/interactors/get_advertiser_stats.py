from ad_platform.application.services.advertiser import AdvertiserService
from ad_platform.application.services.stats_service import StatsService
from ad_platform.domain.entities import AdvertiserId, DailyStats, Stats
from ad_platform.infrastructure.db.commiter import Commiter


class GetAdvertiserStatsInteractor:
    def __init__(
        self,
        advertiser_service: AdvertiserService,
        stats_service: StatsService,
        commiter: Commiter,
    ) -> None:
        self.advertiser_service = advertiser_service
        self.stats_service = stats_service
        self.commiter = commiter

    async def __call__(self, advertiser_id: AdvertiserId) -> Stats:
        async with self.commiter:
            await self.advertiser_service.ensure_advertiser_exists(advertiser_id)

            return await self.stats_service.get_advertiser_stats(advertiser_id)


class GetAdvertiserDailyStatsInteractor:
    def __init__(
        self,
        advertiser_service: AdvertiserService,
        stats_service: StatsService,
        commiter: Commiter,
    ) -> None:
        self.advertiser_service = advertiser_service
        self.stats_service = stats_service
        self.commiter = commiter

    async def __call__(self, advertiser_id: AdvertiserId) -> DailyStats:
        async with self.commiter:
            await self.advertiser_service.ensure_advertiser_exists(advertiser_id)

            return await self.stats_service.get_advertiser_daily_stats(advertiser_id)
