from ad_platform.domain.entities import CampaignId, Click, ClientId, Impression
from ad_platform.domain.exceptions import (
    AdAlreadyClickedError,
    AdWasNotShownBeforeError,
)
from ad_platform.infrastructure.db.gateways.common import ActionsGateway


class AdsService:
    def __init__(self, action_gateway: ActionsGateway) -> None:
        self.action_gateway = action_gateway

    async def create_impression(self, impression: Impression) -> None:
        await self.action_gateway.create_impression(impression)

    async def create_click(self, click: Click) -> None:
        await self.action_gateway.create_click(click)

    async def ensure_ad_shown(
        self,
        client_id: ClientId,
        campaign_id: CampaignId,
    ) -> None:
        res = await self.action_gateway.get_impression(campaign_id, client_id)

        if res is None:
            raise AdWasNotShownBeforeError

    async def ensure_ad_not_clicked(
        self,
        client_id: ClientId,
        campaign_id: CampaignId,
    ) -> None:
        res = await self.action_gateway.get_click(campaign_id, client_id)

        if res is not None:
            raise AdAlreadyClickedError
