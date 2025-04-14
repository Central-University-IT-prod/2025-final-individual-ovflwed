from ad_platform.application.services.ads import AdsService
from ad_platform.application.services.campaigns import CampaignService
from ad_platform.application.services.client import ClientService
from ad_platform.application.services.time import TimeService
from ad_platform.domain.entities import ClientId, Impression, UserCampaign
from ad_platform.infrastructure.db.commiter import Commiter


class GetAdInteractor:
    def __init__(
        self,
        campaign_service: CampaignService,
        client_service: ClientService,
        ads_service: AdsService,
        time_service: TimeService,
        commiter: Commiter,
    ) -> None:
        self.campaign_service = campaign_service
        self.time_service = time_service
        self.client_service = client_service
        self.ads_service = ads_service
        self.commiter = commiter

    async def __call__(self, client_id: ClientId) -> UserCampaign:
        async with self.commiter:
            now = await self.time_service.get_time()
            client = await self.client_service.get_client(client_id)

            campaign = await self.campaign_service.get_target_campaign(now, client)
            await self.ads_service.create_impression(
                Impression(
                    campaign_id=campaign.campaign_id,
                    client_id=client_id,
                    day=now,
                    price=campaign.cost_per_impression,
                ),
            )

        return UserCampaign(
            ad_id=campaign.campaign_id,
            ad_title=campaign.ad_title,
            ad_text=campaign.ad_text,
            advertiser_id=campaign.advertiser_id,
            image_url=campaign.image_url,
        )
