from ad_platform.application.services.advertiser import AdvertiserService
from ad_platform.application.services.campaigns import CampaignService
from ad_platform.domain.entities import AdvertiserId, Campaign
from ad_platform.infrastructure.db.commiter import Commiter


class GetCampaignsInteractor:
    def __init__(
        self,
        campaign_service: CampaignService,
        advertiser_service: AdvertiserService,
        commiter: Commiter,
    ) -> None:
        self.campaign_service = campaign_service
        self.advertiser_service = advertiser_service
        self.commiter = commiter

    async def __call__(
        self,
        advertiser_id: AdvertiserId,
        page: int,
        size: int,
    ) -> list[Campaign]:
        async with self.commiter:
            await self.advertiser_service.ensure_advertiser_exists(advertiser_id)

            return await self.campaign_service.get_campaigns(
                advertiser_id,
                page,
                size,
            )
