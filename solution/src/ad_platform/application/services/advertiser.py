from ad_platform.domain.entities import Advertiser, AdvertiserId, Score
from ad_platform.domain.exceptions import NotFoundError
from ad_platform.infrastructure.db.commiter import Commiter
from ad_platform.infrastructure.db.gateways.common import (
    AdvertiserGateway,
    ClientGateway,
    ScoresGateway,
)


class AdvertiserService:
    def __init__(
        self,
        advertiser_gateway: AdvertiserGateway,
        score_gateway: ScoresGateway,
        client_gateway: ClientGateway,
        commiter: Commiter,
    ) -> None:
        self.advertiser_gateway = advertiser_gateway
        self.client_gateway = client_gateway
        self.score_gateway = score_gateway
        self.commiter = commiter

    async def get_advertiser(self, advertiser_id: AdvertiserId) -> Advertiser:
        res = await self.advertiser_gateway.get_advertiser(advertiser_id)

        if res is None:
            raise NotFoundError

        return res

    async def upsert_advertisers(
        self,
        advertisers: list[Advertiser],
    ) -> list[Advertiser]:
        async with self.commiter:
            await self.advertiser_gateway.upsert_advertisers(advertisers)

        return advertisers

    async def upsert_score(self, score: Score) -> None:
        await self.score_gateway.upsert_score(score)

    async def ensure_advertiser_exists(self, advertiser_id: AdvertiserId) -> None:
        res = await self.advertiser_gateway.get_advertiser(advertiser_id)

        if res is None:
            raise NotFoundError
