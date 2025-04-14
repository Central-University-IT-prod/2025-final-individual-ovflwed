from io import BytesIO

from ad_platform.application.services.advertiser import AdvertiserService
from ad_platform.application.services.campaigns import CampaignService
from ad_platform.application.services.time import TimeService
from ad_platform.domain.entities import AdvertiserId, Campaign, CampaignId
from ad_platform.domain.exceptions import BusinessValidationError
from ad_platform.infrastructure.db.commiter import Commiter


class UpdateCampaignInteractor:
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
        async with self.commiter:
            campaign_db = await self.campaign_service.get_campaign(
                campaign.campaign_id,
                campaign.advertiser_id,
            )

            day = await self.time_service.get_time()

            if day >= campaign_db.start_date and (
                campaign_db.clicks_limit != campaign.clicks_limit
                or campaign_db.impressions_limit != campaign.impressions_limit
                or campaign_db.start_date != campaign.start_date
                or campaign_db.end_date != campaign.end_date
            ):
                raise BusinessValidationError(
                    detail="Нельзя обновить данные параметры активной кампании.",
                )

            if campaign.start_date <= day:
                raise BusinessValidationError(
                    detail="Нельзя обновить данные параметры активной кампании.",
                )

            if campaign.end_date < campaign.start_date:
                raise BusinessValidationError(
                    detail="Некорректные данные запроса.",
                )

            if campaign_db.image_url != campaign.image_url:
                msg = "Нельзя обновить изображение вручную."
                raise BusinessValidationError(msg)

            await self.campaign_service.update_campaign(campaign)

        return await self.campaign_service.get_campaign(
            campaign.campaign_id,
            campaign.advertiser_id,
        )


class UpdateCampaignImageInteractor:
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
        filename: str,
        image: BytesIO,
    ) -> None:
        async with self.commiter:
            await self.campaign_service.get_campaign(
                campaign_id,
                advertiser_id,
            )

            if filename is None and image is None:
                await self.campaign_service.delete_image(campaign_id)
                return

            if not filename.endswith(".jpeg") and not filename.endswith(".jpg"):
                msg = "Неверное расширение файла."
                raise BusinessValidationError(msg)

            await self.campaign_service.upsert_image(campaign_id, image)
