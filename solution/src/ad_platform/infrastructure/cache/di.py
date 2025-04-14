from dishka import Provider, Scope
from redis.asyncio import Redis

from ad_platform.infrastructure.cache.common import CacheGateway
from ad_platform.infrastructure.cache.config import CacheConfig, get_cache_config
from ad_platform.infrastructure.cache.impl import CacheGatewayImpl


async def get_cache_connection(config: CacheConfig) -> Redis:
    return await Redis.from_url(f"redis://{config.host}:{config.port}")


def get_cache_provider() -> Provider:
    provider = Provider()

    provider.provide(get_cache_config, scope=Scope.APP)
    provider.provide(get_cache_connection, scope=Scope.APP)
    provider.provide(CacheGatewayImpl, scope=Scope.REQUEST, provides=CacheGateway)

    return provider
