from ad_platform.application.services.advertiser import AdvertiserService
from ad_platform.application.services.client import ClientService
from ad_platform.domain.entities import Score
from ad_platform.infrastructure.db.commiter import Commiter


class CreateScoreInteractor:
    def __init__(
        self,
        advertiser_service: AdvertiserService,
        client_service: ClientService,
        commiter: Commiter,
    ) -> None:
        self.advertiser_service = advertiser_service
        self.client_service = client_service
        self.commiter = commiter

    async def __call__(self, score: Score) -> None:
        async with self.commiter:
            await self.advertiser_service.ensure_advertiser_exists(score.advertiser_id)
            await self.client_service.ensure_client_exists(score.client_id)
            await self.advertiser_service.upsert_score(score)
