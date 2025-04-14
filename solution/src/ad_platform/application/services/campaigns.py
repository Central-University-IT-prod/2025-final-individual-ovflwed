from io import BytesIO
from uuid import uuid4

from ad_platform.domain.entities import AdvertiserId, Campaign, CampaignId, Client
from ad_platform.domain.exceptions import NotFoundError
from ad_platform.infrastructure.db.commiter import Commiter
from ad_platform.infrastructure.db.gateways.common import CampaignGateway
from ad_platform.infrastructure.storage.common import ImageGateway
from ad_platform.infrastructure.storage.config import StorageConfig


class CampaignService:
    def __init__(
        self,
        campaign_gateway: CampaignGateway,
        images_gateway: ImageGateway,
        config: StorageConfig,
        commiter: Commiter,
    ) -> None:
        self.campaign_gateway = campaign_gateway
        self.images_gateway = images_gateway
        self.cdn_url = config.cdn
        self.commiter = commiter

    async def get_campaign(
        self,
        campaign_id: CampaignId,
        advertiser_id: AdvertiserId | None = None,
    ) -> Campaign:
        campaign = await self.campaign_gateway.get_campaign(campaign_id)

        if campaign is None:
            raise NotFoundError

        if advertiser_id is not None and campaign.advertiser_id != advertiser_id:
            raise NotFoundError

        if campaign.image_url is not None:
            campaign.image_url = self.cdn_url + campaign.image_url

        return campaign

    async def get_campaigns(
        self,
        advertiser_id: AdvertiserId,
        page: int,
        size: int,
    ) -> list[Campaign]:
        campaigns = await self.campaign_gateway.get_campaigns(advertiser_id, page, size)

        for campaign in campaigns:
            if campaign.image_url is not None:
                campaign.image_url = self.cdn_url + campaign.image_url

        return campaigns

    async def create_campaign(self, campaign: Campaign) -> Campaign:
        await self.campaign_gateway.create_campaign(campaign)

        return campaign

    async def update_campaign(self, campaign: Campaign) -> Campaign:
        await self.campaign_gateway.update_campaign(campaign)

        if campaign.image_url is not None:
            campaign.image_url = self.cdn_url + campaign.image_url

        return campaign

    async def delete_campaign(self, campaign_id: CampaignId) -> None:
        await self.campaign_gateway.delete_campaign(campaign_id)

    async def upsert_image(self, campaign_id: CampaignId, image: BytesIO) -> str:
        image_id = str(uuid4()) + ".jpg"

        await self.images_gateway.put(image, image_id)
        await self.campaign_gateway.update_campaign_image(
            campaign_id,
            image_id,
        )

        return self.cdn_url + image_id

    async def get_target_campaign(self, day: int, client: Client) -> Campaign:
        res = await self.campaign_gateway.get_target_campaign(
            day,
            client.gender,
            client.age,
            client.location,
            client.client_id,
        )

        if res is None:
            raise NotFoundError(detail="Нет доступных объявлений.")

        if res.image_url is not None:
            res.image_url = self.cdn_url + res.image_url

        return res

    async def ensure_campaign_exists(self, campaign_id: CampaignId) -> None:
        campaign = await self.campaign_gateway.get_campaign(campaign_id)

        if campaign is None:
            raise NotFoundError

    async def delete_image(self, campaign_id: CampaignId) -> None:
        await self.campaign_gateway.update_campaign_image(campaign_id, None)

    async def ensure_campaign_exists_ever(self, campaign_id: CampaignId) -> None:
        campaign = await self.campaign_gateway.get_campaign_deleted(campaign_id)

        if campaign is None:
            raise NotFoundError
