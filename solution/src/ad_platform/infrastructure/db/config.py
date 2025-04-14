import os
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DBConfig:
    host: str
    port: int
    user: str
    password: str


def get_db_config() -> DBConfig:
    return DBConfig(
        host=os.getenv("POSTGRES_HOST"),
        port=int(os.getenv("POSTGRES_PORT")),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )
