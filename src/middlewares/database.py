from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from starlette.requests import Request


class DatabaseMiddleware:
    def __init__(self, sessionmaker: async_sessionmaker[AsyncSession]):
        self._async_sessionmaker = sessionmaker

    async def __call__(self, request: Request, call_next):
        request.state.database_session = self._async_sessionmaker
        response = await call_next(request)
        return response
