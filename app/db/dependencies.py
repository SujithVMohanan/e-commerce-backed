
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import SessionFactory


async def get_db() -> AsyncGenerator[AsyncSession, None]:

    async with SessionFactory() as session:

        try:
            yield session

        except Exception:
            await session.rollback()
            raise
