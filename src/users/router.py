from typing import Annotated

from fastapi import APIRouter, Depends

from async_fastapi_jwt_auth import AuthJWT

from sqlalchemy.ext.asyncio import AsyncSession

from .repositories import UserRepository
from .schemas import UserAccessTokenSchema
from src.dependencies import get_database_session

router = APIRouter()


@router.post('/users', response_model=UserAccessTokenSchema)
async def register_user(
        name: str,
        login: str,
        password: str,
        database: Annotated[AsyncSession, Depends(get_database_session)],
        authorize: AuthJWT = Depends()
):
    user_id = await UserRepository(database).create_one(name=name, login=login, password=password)
    access_token = await authorize.create_access_token(subject=user_id)

    return UserAccessTokenSchema(
        access_token=access_token
    )
