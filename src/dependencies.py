from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request


async def get_database_session(request: Request) -> AsyncSession:
    if not hasattr(request.state, 'database_session'):
        return
    session = request.state.database_session()
    try:
        yield session
    finally:
        await session.close()
