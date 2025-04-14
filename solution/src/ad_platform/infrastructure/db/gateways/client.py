import logging
from typing import cast

from asyncpg import Connection

from ad_platform.domain.entities import Client, ClientGender, ClientId
from ad_platform.infrastructure.db.gateways.common import ClientGateway

logger = logging.getLogger(__name__)


class ClientGatewayImpl(ClientGateway):
    def __init__(self, conn: Connection) -> None:
        self.conn = conn

    async def get_client(self, client_id: ClientId) -> Client | None:
        logger.info("Getting client %s", client_id)

        client = await self.conn.fetchrow(
            "SELECT client_id, login, age, loc, gender FROM clients WHERE client_id = $1",
            client_id,
        )

        if not client:
            return None

        return Client(
            client_id=cast(ClientId, client["client_id"]),
            login=client["login"],
            age=client["age"],
            location=client["loc"],
            gender=ClientGender[client["gender"]],
        )

    async def upsert_clients(self, clients: list[Client]) -> None:
        logger.info(
            "Upserting %s clients: %s",
            len(clients),
            [x.client_id for x in clients],
        )

        await self.conn.executemany(
            """
            INSERT INTO clients (client_id, login, age, loc, gender)
            VALUES
                ($1, $2, $3, $4, $5)
            ON CONFLICT
                (client_id)
            DO UPDATE
            SET
                login = $2, age = $3, loc = $4, gender = $5;
            """,
            [
                (
                    client.client_id,
                    client.login,
                    client.age,
                    client.location,
                    client.gender.value,
                )
                for client in clients
            ],
        )
