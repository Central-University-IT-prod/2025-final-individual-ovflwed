from dishka import Provider, Scope

from ad_platform.application.interactors.click_ad import ClickAdInteractor
from ad_platform.application.interactors.create_campaign import CreateCampaignInteractor
from ad_platform.application.interactors.create_score import CreateScoreInteractor
from ad_platform.application.interactors.delete_campaign import DeleteCampaignInteractor
from ad_platform.application.interactors.get_ad import GetAdInteractor
from ad_platform.application.interactors.get_advertiser_stats import (
    GetAdvertiserDailyStatsInteractor,
    GetAdvertiserStatsInteractor,
)
from ad_platform.application.interactors.get_campaign_stats import (
    GetCampaignDailyStatsInteractor,
    GetCampaignStatsInteractor,
)
from ad_platform.application.interactors.get_campaigns import GetCampaignsInteractor
from ad_platform.application.interactors.update_campaign import (
    UpdateCampaignImageInteractor,
    UpdateCampaignInteractor,
)


def get_interactor_provider() -> Provider:
    provider = Provider()

    provider.provide(CreateScoreInteractor, scope=Scope.REQUEST)
    provider.provide(CreateCampaignInteractor, scope=Scope.REQUEST)
    provider.provide(DeleteCampaignInteractor, scope=Scope.REQUEST)
    provider.provide(UpdateCampaignInteractor, scope=Scope.REQUEST)
    provider.provide(GetCampaignsInteractor, scope=Scope.REQUEST)
    provider.provide(GetAdInteractor, scope=Scope.REQUEST)
    provider.provide(ClickAdInteractor, scope=Scope.REQUEST)
    provider.provide(GetAdvertiserDailyStatsInteractor, scope=Scope.REQUEST)
    provider.provide(GetAdvertiserStatsInteractor, scope=Scope.REQUEST)
    provider.provide(GetCampaignDailyStatsInteractor, scope=Scope.REQUEST)
    provider.provide(GetCampaignStatsInteractor, scope=Scope.REQUEST)
    provider.provide(UpdateCampaignImageInteractor, scope=Scope.REQUEST)

    return provider
