from ad_platform.application.services.advertiser import AdvertiserService
from ad_platform.application.services.campaigns import CampaignService
from ad_platform.domain.entities import AdvertiserId, CampaignId
from ad_platform.infrastructure.db.commiter import Commiter


class DeleteCampaignInteractor:
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
        campaign_id: CampaignId,
        advertiser_id: AdvertiserId,
    ) -> None:
        async with self.commiter:
            campaign = await self.campaign_service.get_campaign(
                campaign_id,
                advertiser_id,
            )

            await self.campaign_service.delete_campaign(campaign_id)

        return campaign
