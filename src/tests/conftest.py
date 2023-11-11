"""Contains test fixtures"""
import asyncio
from contextlib import suppress
from typing import AsyncGenerator, Generator

from httpx import AsyncClient
import pytest
import pytest_asyncio
from sqlalchemy import text
from sqlalchemy.engine import make_url, URL
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from core.config import app_settings
from db.db import get_session
from main import app
from models.base import Base


@pytest_asyncio.fixture(scope='session', autouse=True)
async def setup_test_database() -> URL:
    """Prepare test database. Functions are slightly adapted from
        https://github.com/igortg/pytest-async-sqlalchemy.
    """
    database_url = make_url(f'{app_settings.database_dsn}_test')
    await create_database(database_url)
    engine = create_async_engine(database_url)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()
    try:
        yield database_url
    finally:
        await drop_database(database_url)


async def create_database(database_url: URL) -> None:
    """Creates test database.

    Args:
        database_url (URL): database URL instance.
    """
    engine = create_async_engine(f"{database_url.drivername}://" +
                                 f"{database_url.username}:{database_url.password}@" +
                                 f"{database_url.host}:{database_url.port}/",
                                 isolation_level="AUTOCOMMIT")
    database_exists = False
    async with engine.connect() as conn:
        with suppress(ProgrammingError):
            check_database = await conn.execute(text('SELECT 1 FROM pg_database WHERE datname=' +
                                                     f'"{database_url.database}"'))
            database_exists = check_database.scalar() == 1
    if database_exists:
        await drop_database(database_url)
    async with engine.connect() as conn:
        await conn.execute(text(f'CREATE DATABASE "{database_url.database}"'))
    await engine.dispose()


async def drop_database(database_url: URL) -> None:
    """Drops test database.

    Args:
        database_url (URL): database URL instance.
    """
    engine = create_async_engine(f"{database_url.drivername}://" +
                                 f"{database_url.username}:{database_url.password}@" +
                                 f"{database_url.host}:{database_url.port}/",
                                 isolation_level="AUTOCOMMIT")
    async with engine.connect() as conn:
        disc_users = """SELECT pg_terminate_backend(pg_stat_activity.%(pid_column)s)
                        FROM pg_stat_activity WHERE pg_stat_activity.datname = '%(database)s'
                        AND %(pid_column)s <> pg_backend_pid();""" % {
                            "pid_column": "pid", "database": database_url.database,}
        await conn.execute(text(disc_users))
        await conn.execute(text(f'DROP DATABASE "{database_url.database}"'))


@pytest.fixture(scope='session')
def event_loop() -> Generator:
    """Creates an instance of the default event loop for the test session"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture()
async def client() -> AsyncGenerator:
    """Creates an async testing client"""
    async with AsyncClient(app=app, base_url='http://testserver') as async_client:
        yield async_client


async def override_get_session() -> AsyncSession:
    """Overrides get_session function.
        https://fastapi.tiangolo.com/advanced/testing-dependencies/
        https://github.com/tiangolo/fastapi/issues/4507?ysclid=loigxnxbfc687176707

    Returns:
        session (AsyncSession): new Session object for test database.
    """
    engine = create_async_engine(f'{app_settings.database_dsn}_test', echo=True, future=True)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session


app.dependency_overrides[get_session] = override_get_session
