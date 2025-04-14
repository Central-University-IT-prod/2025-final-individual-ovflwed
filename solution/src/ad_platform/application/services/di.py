from dishka import Provider, Scope

from ad_platform.application.services.ads import AdsService
from ad_platform.application.services.advertiser import AdvertiserService
from ad_platform.application.services.campaigns import CampaignService
from ad_platform.application.services.client import ClientService
from ad_platform.application.services.stats_service import StatsService
from ad_platform.application.services.time import TimeService


def get_service_provider() -> Provider:
    provider = Provider()

    provider.provide(AdvertiserService, scope=Scope.REQUEST)
    provider.provide(ClientService, scope=Scope.REQUEST)
    provider.provide(CampaignService, scope=Scope.REQUEST)
    provider.provide(TimeService, scope=Scope.REQUEST)
    provider.provide(AdsService, scope=Scope.REQUEST)
    provider.provide(StatsService, scope=Scope.REQUEST)

    return provider
