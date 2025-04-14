from ad_platform.infrastructure.cache.common import CacheGateway
from ad_platform.infrastructure.db.commiter import Commiter
from ad_platform.infrastructure.db.gateways.common import TimeGateway


class TimeService:
    def __init__(
        self,
        time_gateway: TimeGateway,
        cache_gateway: CacheGateway,
        commiter: Commiter,
    ) -> None:
        self.time_gateway = time_gateway
        self.cache_gateway = cache_gateway
        self.commiter = commiter

    async def get_time(self) -> int:
        cached = await self.cache_gateway.get("time")
        if cached is not None:
            return int(cached)

        time = await self.time_gateway.get_time()

        await self.cache_gateway.set("time", str(time))

        return time

    async def advance_time(self, time: int) -> int:
        async with self.commiter:
            await self.time_gateway.advance_time(time)
            await self.cache_gateway.set("time", str(time))

        return time
