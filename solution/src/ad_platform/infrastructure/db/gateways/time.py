from asyncpg import Connection

from ad_platform.infrastructure.db.gateways.common import TimeGateway


class TimeGatewayImpl(TimeGateway):
    def __init__(self, conn: Connection) -> None:
        self.conn = conn

    async def get_time(self) -> int:
        res = await self.conn.fetchval("SELECT day FROM day")
        if res is None:
            await self.conn.execute("INSERT INTO day (day) VALUES (0)")
            res = 0

        return res

    async def advance_time(self, time: int) -> None:
        await self.conn.execute("UPDATE day SET day = $1", time)
