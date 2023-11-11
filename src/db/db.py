"""Contains code responsible for connecting to the database"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from core.config import app_settings


# an Engine, which the Session will use for connection
engine = create_async_engine(app_settings.database_dsn.unicode_string(), echo=True, future=True)
# generate Session object
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_session() -> AsyncSession:
    """Required for Dependency injection.

    Returns:
        session (AsyncSession): new Session object.
    """
    async with async_session() as session:
        yield session
