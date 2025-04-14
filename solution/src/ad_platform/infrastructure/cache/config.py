import os
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CacheConfig:
    host: str
    port: int


def get_cache_config() -> CacheConfig:
    return CacheConfig(
        host=os.getenv("REDIS_HOST"),
        port=int(os.getenv("REDIS_PORT")),
    )
