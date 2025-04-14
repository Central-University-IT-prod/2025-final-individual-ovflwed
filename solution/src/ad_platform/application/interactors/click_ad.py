import logging

from ad_platform.application.interactors.create_score import ClientService
from ad_platform.application.services.ads import AdAlreadyClickedError, AdsService
from ad_platform.application.services.campaigns import CampaignService
from ad_platform.application.services.time import TimeService
from ad_platform.domain.entities import CampaignId, Click, ClientId
from ad_platform.infrastructure.db.commiter import Commiter

logger = logging.getLogger(__name__)


class ClickAdInteractor:
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

    async def __call__(self, client_id: ClientId, campaign_id: CampaignId) -> None:
        async with self.commiter:
            await self.client_service.ensure_client_exists(client_id)
            campaign = await self.campaign_service.get_campaign(campaign_id)
            logger.info("Clicking ad %s for client %s", campaign, client_id)

            try:
                await self.ads_service.ensure_ad_not_clicked(client_id, campaign_id)
            except AdAlreadyClickedError:
                return

            await self.ads_service.ensure_ad_shown(client_id, campaign_id)

            await self.ads_service.create_click(
                Click(
                    campaign_id,
                    client_id,
                    await self.time_service.get_time(),
                    campaign.cost_per_click,
                ),
            )
