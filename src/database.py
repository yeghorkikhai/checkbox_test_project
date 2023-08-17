import os

from dotenv import load_dotenv

from sqlalchemy import URL
from sqlalchemy.ext.asyncio import (
    create_async_engine as _create_async_engine,
    async_sessionmaker,
    AsyncEngine,
    AsyncSession
)

load_dotenv(os.path.abspath('.env'))

DATABASE_URL = URL.create(
    'postgresql+asyncpg',
    host=os.getenv('DATABASE_HOST'),
    port=os.getenv('DATABASE_PORT'),
    username=os.getenv('DATABASE_USER'),
    password=os.getenv('DATABASE_PASSWORD'),
    database=os.getenv('DATABASE_NAME')
)


class Database:
    def __init__(self, url: URL = DATABASE_URL):
        self._async_engine: AsyncEngine = _create_async_engine(url)
        self._async_session_maker: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self._async_engine,
            expire_on_commit=False
        )

    @property
    def engine(self) -> AsyncEngine:
        return self._async_engine

    @property
    def sessionmaker(self) -> async_sessionmaker[AsyncSession]:
        return self._async_session_maker
