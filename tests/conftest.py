import asyncio
import os
import pytest

from dotenv import load_dotenv

from sqlalchemy import URL
from sqlalchemy.pool import NullPool
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
    async_sessionmaker as _async_sessionmaker
)

from typing import AsyncGenerator

from starlette.testclient import TestClient
from httpx import AsyncClient

from src.dependencies import get_database_session
from src.main import app
from src.models import Base

load_dotenv(os.path.abspath('.env'))

TEST_DATABASE_URL = URL.create(
    'postgresql+asyncpg',
    host=os.getenv('TEST_DATABASE_HOST'),
    port=os.getenv('TEST_DATABASE_PORT'),
    username=os.getenv('TEST_DATABASE_USER'),
    password=os.getenv('TEST_DATABASE_PASSWORD'),
    database=os.getenv('TEST_DATABASE_NAME')
)

engine_test: AsyncEngine = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)
async_sessionmaker = _async_sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)
Base.metadata.bind = engine_test


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_sessionmaker() as session:
        yield session


app.dependency_overrides[get_database_session] = override_get_async_session


# @pytest.fixture(autouse=True, scope='session')
# async def prepare_database():
#     async with engine_test.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#         await conn.commit()
#     yield
#     async with engine_test.connect() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.commit()


@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


client = TestClient(app)


@pytest.fixture(scope='session')
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac




