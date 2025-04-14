from abc import abstractmethod
from typing import Protocol

from ad_platform.domain.entities import (
    Advertiser,
    AdvertiserId,
    Campaign,
    CampaignId,
    Click,
    Client,
    ClientGender,
    ClientId,
    Impression,
    Score,
    Stats,
)


class ClientGateway(Protocol):
    @abstractmethod
    async def get_client(self, client_id: ClientId) -> Client | None: ...
    @abstractmethod
    async def upsert_clients(self, clients: list[Client]) -> None: ...


class AdvertiserGateway(Protocol):
    @abstractmethod
    async def get_advertiser(
        self,
        advertiser_id: AdvertiserId,
    ) -> Advertiser | None: ...
    @abstractmethod
    async def upsert_advertisers(self, advertisers: list[Advertiser]) -> None: ...


class ScoresGateway(Protocol):
    @abstractmethod
    async def upsert_score(self, score: Score) -> None: ...


class CampaignGateway(Protocol):
    @abstractmethod
    async def get_campaign(self, campaign_id: CampaignId) -> Campaign | None: ...

    @abstractmethod
    async def get_campaigns(
        self,
        advertiser_id: AdvertiserId,
        page: int,
        size: int,
    ) -> list[Campaign]: ...

    @abstractmethod
    async def create_campaign(self, campaign: Campaign) -> None: ...
    @abstractmethod
    async def update_campaign(self, campaign: Campaign) -> None: ...
    @abstractmethod
    async def delete_campaign(self, campaign_id: CampaignId) -> None: ...
    @abstractmethod
    async def update_campaign_image(
        self,
        campaign_id: CampaignId,
        image_url: str,
    ) -> None: ...
    @abstractmethod
    async def get_target_campaign(
        self,
        day: int,
        gender: ClientGender,
        age: int,
        location: str,
        client_id: ClientId,
    ) -> Campaign | None: ...
    @abstractmethod
    async def get_campaign_deleted(
        self,
        campaign_id: CampaignId,
    ) -> Campaign | None: ...


class TimeGateway(Protocol):
    @abstractmethod
    async def get_time(self) -> int: ...
    @abstractmethod
    async def advance_time(self, time: int) -> None: ...


class ActionsGateway(Protocol):
    @abstractmethod
    async def create_impression(self, impression: Impression) -> None: ...
    @abstractmethod
    async def create_click(self, click: Click) -> None: ...
    @abstractmethod
    async def get_impression(
        self,
        campaign_id: CampaignId,
        client_id: ClientId,
    ) -> Impression | None: ...
    @abstractmethod
    async def get_click(
        self,
        campaign_id: CampaignId,
        client_id: ClientId,
    ) -> Click | None: ...
    @abstractmethod
    async def get_campaign_stats(self, campaign_id: CampaignId) -> Stats: ...
    @abstractmethod
    async def get_advertiser_stats(self, advertiser_id: AdvertiserId) -> Stats: ...
    @abstractmethod
    async def get_campaign_daily_stats(
        self,
        campaign_id: CampaignId,
    ) -> list[Stats]: ...
    @abstractmethod
    async def get_advertiser_daily_stats(
        self,
        advertiser_id: AdvertiserId,
    ) -> list[Stats]: ...
