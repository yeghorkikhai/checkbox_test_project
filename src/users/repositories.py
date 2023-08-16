from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_one(
            self,
            name: str,
            login: str,
            password: str
    ) -> int:
        user: User = User(
            name=name,
            login=login,
            password=password
        )
        self._session.add(user)

        await self._session.flush()
        user_id = user.id
        await self._session.commit()

        return user_id

    async def get(self, user_id: int) -> User | None:
        statement = select(User).where(User.id == user_id)
        result = await self._session.execute(statement)
        return result.scalar_one_or_none()
