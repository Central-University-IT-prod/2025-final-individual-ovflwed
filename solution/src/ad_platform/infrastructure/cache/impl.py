from typing import cast

from redis.asyncio import Redis

from ad_platform.infrastructure.cache.common import CacheGateway


class CacheGatewayImpl(CacheGateway):
    def __init__(self, cache: Redis) -> None:
        self.cache = cache

    async def get(self, key: str) -> str | None:
        return cast(str | None, await self.cache.get(key))

    async def set(self, key: str, value: str) -> None:
        await self.cache.set(key, value)
