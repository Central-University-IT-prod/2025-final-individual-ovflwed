from uuid import uuid4

from ad_platform.application.services.advertiser import AdvertiserService
from ad_platform.application.services.campaigns import CampaignService
from ad_platform.application.services.time import TimeService
from ad_platform.domain.entities import Campaign
from ad_platform.domain.exceptions import BusinessValidationError
from ad_platform.infrastructure.db.commiter import Commiter


class CreateCampaignInteractor:
    def __init__(
        self,
        campaign_service: CampaignService,
        advertiser_service: AdvertiserService,
        time_service: TimeService,
        commiter: Commiter,
    ) -> None:
        self.campaign_service = campaign_service
        self.advertiser_service = advertiser_service
        self.time_service = time_service
        self.commiter = commiter

    async def __call__(self, campaign: Campaign) -> Campaign:
        day = await self.time_service.get_time()
        campaign.campaign_id = uuid4()

        if day > campaign.start_date or day > campaign.end_date:
            raise BusinessValidationError(
                detail="Нельзя создать рекламную кампанию в прошлом.",
            )

        async with self.commiter:
            await self.advertiser_service.ensure_advertiser_exists(
                campaign.advertiser_id,
            )
            await self.campaign_service.create_campaign(campaign)

        return campaign
