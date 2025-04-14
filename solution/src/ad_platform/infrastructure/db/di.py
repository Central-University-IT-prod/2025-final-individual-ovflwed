from collections.abc import AsyncIterator

from asyncpg import Connection, Pool, create_pool
from dishka import Provider, Scope

from ad_platform.infrastructure.db.commiter import Commiter, CommiterImpl
from ad_platform.infrastructure.db.config import DBConfig, get_db_config
from ad_platform.infrastructure.db.gateways.ads import ActionsGatewayImpl
from ad_platform.infrastructure.db.gateways.advertiser import AdvertiserGatewayImpl
from ad_platform.infrastructure.db.gateways.campaign import CampaignGatewayImpl
from ad_platform.infrastructure.db.gateways.client import ClientGatewayImpl
from ad_platform.infrastructure.db.gateways.common import (
    ActionsGateway,
    AdvertiserGateway,
    CampaignGateway,
    ClientGateway,
    ScoresGateway,
    TimeGateway,
)
from ad_platform.infrastructure.db.gateways.scores import ScoresGatewayImpl
from ad_platform.infrastructure.db.gateways.time import TimeGatewayImpl


async def get_db_pool(config: DBConfig) -> Pool:
    return await create_pool(
        host=config.host,
        port=config.port,
        user=config.user,
        password=config.password,
    )


async def get_db_connection(pool: Pool) -> AsyncIterator[Connection]:
    conn = await pool.acquire()

    yield conn

    await pool.release(conn)


def get_commiter(conn: Connection) -> CommiterImpl:
    return CommiterImpl(conn)


def get_client_gateway(conn: Connection) -> ClientGatewayImpl:
    return ClientGatewayImpl(conn)


def get_advertiser_gateway(conn: Connection) -> AdvertiserGatewayImpl:
    return AdvertiserGatewayImpl(conn)


def get_score_gateway(conn: Connection) -> ScoresGatewayImpl:
    return ScoresGatewayImpl(conn)


def get_campaign_gateway(conn: Connection) -> CampaignGatewayImpl:
    return CampaignGatewayImpl(conn)


def get_time_gateway(conn: Connection) -> TimeGatewayImpl:
    return TimeGatewayImpl(conn)


def get_actions_gateway(conn: Connection) -> ActionsGatewayImpl:
    return ActionsGatewayImpl(conn)


def get_db_provider() -> Provider:
    provider = Provider()

    provider.provide(get_db_config, scope=Scope.APP)
    provider.provide(get_db_pool, scope=Scope.APP)
    provider.provide(get_db_connection, scope=Scope.REQUEST)
    provider.provide(get_commiter, scope=Scope.REQUEST, provides=Commiter)
    provider.provide(get_client_gateway, scope=Scope.REQUEST, provides=ClientGateway)
    provider.provide(
        get_advertiser_gateway,
        scope=Scope.REQUEST,
        provides=AdvertiserGateway,
    )
    provider.provide(get_score_gateway, scope=Scope.REQUEST, provides=ScoresGateway)
    provider.provide(get_time_gateway, scope=Scope.REQUEST, provides=TimeGateway)
    provider.provide(
        get_campaign_gateway,
        scope=Scope.REQUEST,
        provides=CampaignGateway,
    )
    provider.provide(get_actions_gateway, scope=Scope.REQUEST, provides=ActionsGateway)

    return provider
