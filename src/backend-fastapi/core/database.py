from collections.abc import AsyncGenerator
from typing import Any
from urllib.parse import urlparse, urlunparse

from loguru import logger
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from ..database.models.base import Base
from .config import BASE_DIR, settings

# --- Connection Configuration ---

connect_args: dict[str, Any] = {
    "prepared_statement_cache_size": 0,
}

db_url = settings.DATABASE_URL

# Handle SSL mode for asyncpg
if "sslmode" in db_url:
    connect_args["ssl"] = "require"
    try:
        parsed = urlparse(db_url)
        # Remove query params (like sslmode) from URL as they are handled in connect_args
        db_url = urlunparse(parsed._replace(query=""))
    except Exception as parse_exc:
        logger.warning(f"Database | action=parse_url_failed error={parse_exc}")

pool_settings: dict[str, Any] = {
    "pool_size": 20,
    "max_overflow": 10,
    "pool_pre_ping": True,
}

async_engine = create_async_engine(
    db_url,
    echo=False,
    connect_args=connect_args,
    **pool_settings,
)

async_session_factory = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for getting async database session.
    """
    async with async_session_factory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def create_db_tables() -> None:
    """
    Create all tables defined in SQLAlchemy models.
    """
    try:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database | action=create_tables status=success")
    except SQLAlchemyError as db_exc:
        logger.error(f"Database | action=create_tables status=failed error={db_exc}")


async def run_alembic_migrations() -> None:
    """
    Run Alembic migrations programmatically using Alembic API.
    """
    import asyncio

    from alembic import command
    from alembic.config import Config

    def _run_sync_migrations() -> None:
        """Synchronous wrapper for Alembic command (runs in thread pool)"""
        try:
            # Path to alembic.ini using BASE_DIR for reliability
            alembic_cfg_path = BASE_DIR / "backend" / "alembic.ini"

            if not alembic_cfg_path.exists():
                logger.warning("Database | action=run_migrations status=skipped reason=alembic_ini_not_found")
                return

            # Create Alembic config
            alembic_cfg = Config(str(alembic_cfg_path))

            # Run migrations (synchronously)
            command.upgrade(alembic_cfg, "head")

            logger.info("Database | action=run_migrations status=success")

        except Exception as exc:
            logger.error(f"Database | action=run_migrations status=failed error={exc}")
            raise

    # Run synchronous function in thread pool
    await asyncio.to_thread(_run_sync_migrations)

# Explicitly export Base for mypy
__all__ = ["Base", "get_db", "create_db_tables", "run_alembic_migrations", "async_engine"]
