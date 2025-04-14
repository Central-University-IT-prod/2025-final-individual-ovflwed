import os
from dataclasses import dataclass


@dataclass
class StorageConfig:
    url: str
    access_key: str
    secret_key: str
    cdn: str


def get_storage_config() -> StorageConfig:
    return StorageConfig(
        url=os.getenv("MINIO_URL"),
        access_key=os.getenv("MINIO_ACCESS_KEY"),
        secret_key=os.getenv("MINIO_SECRET_KEY"),
        cdn=os.getenv("CDN_URL"),
    )
