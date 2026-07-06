"""Migration runner — executes idempotent SQL migrations on startup."""

import os
from pathlib import Path

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from app.core.config import settings


async def run_migrations():
    """Run all idempotent SQL migrations from backend/migrations/."""
    engine = create_async_engine(settings.database_url)
    migrations_dir = Path(__file__).parent.parent.parent / "migrations"

    if not migrations_dir.exists():
        return

    async with engine.begin() as conn:
        for migration_file in sorted(migrations_dir.glob("*.sql")):
            sql = migration_file.read_text()
            await conn.execute(text(sql))

    await engine.dispose()


if __name__ == "__main__":
    import asyncio

    asyncio.run(run_migrations())
