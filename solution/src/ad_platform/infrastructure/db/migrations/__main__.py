import asyncio
import logging
from pathlib import Path

import asyncpg

from ad_platform.infrastructure.db.config import DBConfig, get_db_config

logger = logging.getLogger("migrations")


async def get_db_connection(config: DBConfig) -> asyncpg.Connection:
    for _ in range(10):
        try:
            return await asyncpg.connect(
                host=config.host,
                port=config.port,
                user=config.user,
                password=config.password,
            )
        except Exception:
            logger.warning("Failed to connect to database")
            await asyncio.sleep(0.5)

    msg = "Failed to connect to database"
    raise Exception(msg)


async def get_applied_migrations(conn: asyncpg.Connection) -> set[str]:
    try:
        rows = await conn.fetch("SELECT migration_id FROM migrations")
    except asyncpg.exceptions.UndefinedTableError:
        await conn.execute(
            """
            CREATE TABLE migrations
            (id SERIAL PRIMARY KEY, migration_id VARCHAR(255) NOT NULL UNIQUE);
            """,
        )
        rows = []

    return {row["migration_id"] for row in rows}


async def apply_migrations(conn: asyncpg.Connection) -> None:
    applied_migrations = await get_applied_migrations(conn)

    migration_files = sorted(Path(__file__).parent.glob("sql/*.sql"))

    for migration_file in migration_files:
        logger.info("Applying migration %s", migration_file)

        migration_id = migration_file.stem

        if migration_id not in applied_migrations:

            with migration_file.open("r") as file:
                sql = file.read()

            await conn.execute(sql)

            await conn.execute(
                "INSERT INTO migrations (migration_id) VALUES ($1)",
                migration_id,
            )


async def main() -> None:
    logging.basicConfig(level=logging.INFO)

    logger.info("Applying migrations")

    conn = await get_db_connection(get_db_config())

    await apply_migrations(conn)

    await conn.close()

    logger.info("Migrations applied")


if __name__ == "__main__":
    asyncio.run(main())
