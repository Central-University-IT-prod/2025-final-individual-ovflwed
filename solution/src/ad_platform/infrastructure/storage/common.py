from abc import abstractmethod
from io import BytesIO
from typing import Protocol


class ImageGateway(Protocol):
    @abstractmethod
    async def put(self, image: BytesIO, name: str) -> None: ...
