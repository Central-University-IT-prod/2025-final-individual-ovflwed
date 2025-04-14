from ad_platform.domain.entities import Client, ClientId
from ad_platform.domain.exceptions import NotFoundError
from ad_platform.infrastructure.db.commiter import Commiter
from ad_platform.infrastructure.db.gateways.common import ClientGateway


class ClientService:
    def __init__(self, client_gateway: ClientGateway, commiter: Commiter) -> None:
        self.client_gateway = client_gateway
        self.commiter = commiter

    async def get_client(self, client_id: ClientId) -> Client:
        res = await self.client_gateway.get_client(client_id)

        if res is None:
            raise NotFoundError

        return res

    async def upsert_clients(self, clients: list[Client]) -> list[Client]:
        async with self.commiter:
            await self.client_gateway.upsert_clients(clients)

        return clients

    async def ensure_client_exists(self, client_id: ClientId) -> None:
        res = await self.client_gateway.get_client(client_id)

        if res is None:
            raise NotFoundError
