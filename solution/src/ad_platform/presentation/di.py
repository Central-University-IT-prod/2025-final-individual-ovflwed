from dishka import AsyncContainer, make_async_container

from ad_platform.application.interactors.di import get_interactor_provider
from ad_platform.application.services.di import get_service_provider
from ad_platform.infrastructure.cache.di import get_cache_provider
from ad_platform.infrastructure.db.di import get_db_provider
from ad_platform.infrastructure.storage.di import get_storage_provider


def create_container() -> AsyncContainer:
    return make_async_container(
        get_db_provider(),
        get_service_provider(),
        get_interactor_provider(),
        get_cache_provider(),
        get_storage_provider(),
    )
