from collections.abc import AsyncIterator

from dishka import Provider, Scope
from miniopy_async import Minio

from ad_platform.infrastructure.storage.common import ImageGateway
from ad_platform.infrastructure.storage.config import StorageConfig, get_storage_config
from ad_platform.infrastructure.storage.impl import ImageGatewayImpl


async def get_session(config: StorageConfig) -> AsyncIterator[Minio]:
    session = Minio(
        config.url,
        access_key=config.access_key,
        secret_key=config.secret_key,
        secure=False,
    )

    yield session


def get_storage_provider() -> Provider:
    provider = Provider()

    provider.provide(get_storage_config, scope=Scope.APP)
    provider.provide(get_session, scope=Scope.APP)
    provider.provide(ImageGatewayImpl, scope=Scope.REQUEST, provides=ImageGateway)

    return provider
