from io import BytesIO

from miniopy_async import Minio

from .common import ImageGateway


class ImageGatewayImpl(ImageGateway):
    def __init__(self, client: Minio) -> None:
        self.client = client
        self.bucket_name = "ad-images"

    async def put(self, image: BytesIO, name: str) -> None:
        await self.client.put_object(
            bucket_name=self.bucket_name,
            object_name=name,
            data=image,
            length=-1,
            part_size=1024 * 1024 * 5,
        )
