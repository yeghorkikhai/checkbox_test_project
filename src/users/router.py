from typing import Annotated

from fastapi import APIRouter, Depends, Body
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from async_fastapi_jwt_auth import AuthJWT

from sqlalchemy.ext.asyncio import AsyncSession

from .repositories import UserRepository
from .schemas import (
    UserAccessTokenSchema,
    UserSchema
)
from src.dependencies import get_database_session
from src.utils.logger import logger

router = APIRouter()

auth_scheme = HTTPBearer()


@logger.catch
@router.post('/users', response_model=UserAccessTokenSchema)
async def register_user(
        name: Annotated[str, Body(min_length=1, max_length=64)],
        login: Annotated[str, Body(min_length=5, max_length=32)],
        password: Annotated[str, Body(min_length=8, max_length=16)],
        database: Annotated[AsyncSession, Depends(get_database_session)],
        authorize: AuthJWT = Depends()
):
    user_id = await UserRepository(database).create_one(name=name, login=login, password=password)
    access_token = await authorize.create_access_token(subject=user_id)

    logger.info(f'UserRegistered: user_id={user_id}')

    return UserAccessTokenSchema(
        access_token=access_token
    )


@logger.catch
@router.get('/users/me', response_model=UserSchema)
async def get_me(
        database: Annotated[AsyncSession, Depends(get_database_session)],
        authorize: AuthJWT = Depends(),
        token: HTTPAuthorizationCredentials = Depends(auth_scheme)
):
    await authorize.jwt_required()
    user_id: int = await authorize.get_jwt_subject()

    logger.info(f'UsersMe: user_id={user_id}')

    user = await UserRepository(database).get(user_id=user_id)

    return UserSchema.model_validate(user, from_attributes=True)
