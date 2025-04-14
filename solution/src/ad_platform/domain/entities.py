from dataclasses import dataclass
from enum import Enum
from typing import NewType, Optional
from uuid import UUID


class Gender(Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    ALL = "ALL"


class ClientGender(Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"


ClientId = NewType("ClientId", UUID)


@dataclass(frozen=True, slots=True)
class Client:
    client_id: ClientId
    login: str
    age: int
    location: str
    gender: ClientGender


AdvertiserId = NewType("AdvertiserId", UUID)


@dataclass(frozen=True, slots=True)
class Advertiser:
    advertiser_id: AdvertiserId
    name: str


@dataclass(frozen=True, slots=True)
class Score:
    client_id: ClientId
    advertiser_id: AdvertiserId
    score: int


CampaignId = NewType("CampaignId", UUID)


@dataclass(frozen=True, slots=True)
class CampaignTarget:
    gender: Optional[Gender]
    age_from: Optional[int]
    age_to: Optional[int]
    location: Optional[str]


@dataclass(slots=True)
class Campaign:
    campaign_id: CampaignId
    advertiser_id: AdvertiserId
    impressions_limit: int
    clicks_limit: int
    cost_per_impression: float
    cost_per_click: float
    ad_title: str
    ad_text: str
    start_date: int
    end_date: int
    image_url: Optional[str]
    targeting: CampaignTarget


@dataclass(slots=True)
class Click:
    campaign_id: CampaignId
    client_id: ClientId
    day: int
    price: float


@dataclass(slots=True)
class Impression:
    campaign_id: CampaignId
    client_id: ClientId
    day: int
    price: float


@dataclass(slots=True)
class UserCampaign:
    ad_id: CampaignId
    ad_title: str
    ad_text: str
    advertiser_id: AdvertiserId
    image_url: Optional[str] = None


@dataclass(slots=True)
class Stats:
    impressions_count: int
    clicks_count: int
    conversion: float
    spent_impressions: float
    spent_clicks: float
    spent_total: float


@dataclass(slots=True)
class DailyStats(Stats):
    date: int
