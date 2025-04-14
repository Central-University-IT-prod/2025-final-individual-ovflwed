import logging
from abc import abstractmethod
from types import TracebackType
from typing import Optional, Protocol, Self

import asyncpg

logger = logging.getLogger(__name__)


class Commiter(Protocol):
    @abstractmethod
    async def begin(self) -> None: ...
    @abstractmethod
    async def commit(self) -> None: ...
    @abstractmethod
    async def rollback(self) -> None: ...
    @abstractmethod
    async def __aenter__(self) -> Self: ...

    @abstractmethod
    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Optional[bool]: ...


class CommiterError(Exception):
    pass


class CommiterImpl(Commiter):
    def __init__(self, conn: asyncpg.Connection) -> None:
        self.conn = conn

    async def begin(self) -> None:
        self.transaction = self.conn.transaction()

        await self.transaction.start()

    async def commit(self) -> None:
        if self.transaction is None:
            msg = "Transaction is not started"
            raise CommiterError(msg)

        await self.transaction.commit()

    async def rollback(self) -> None:
        if self.transaction is None:
            msg = "Transaction is not started"
            raise CommiterError(msg)

        await self.transaction.rollback()

    async def __aenter__(self) -> Self:
        logger.info("Begin transaction")
        await self.begin()

        return self

    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Optional[bool]:
        if exc_type is None:
            logger.info("Commit transaction")
            await self.commit()
        else:
            logger.info("Rollback transaction")
            await self.rollback()

        return False
