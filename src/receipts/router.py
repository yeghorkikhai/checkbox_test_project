from typing import Annotated

from fastapi import APIRouter, Depends, Query, Body

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from fastapi.responses import PlainTextResponse

from async_fastapi_jwt_auth import AuthJWT

from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies import get_database_session

from .repositories import ReceiptRepository
from src.users.repositories import UserRepository

from src.receipts.enums import PaymentType
from src.receipts.schemas import (
    ProductSchema,
    PaymentSchema,
    ReceiptSchema
)
from src.users.schemas import UserSchema

from .utils import generate_text_receipt
from src.utils.logger import logger

router = APIRouter()

auth_scheme = HTTPBearer()


@logger.catch
@router.post('/receipts', response_model=ReceiptSchema)
async def create_receipt(
        products: Annotated[list[ProductSchema], Body(min_length=1)],
        payment: PaymentSchema,
        database: Annotated[AsyncSession, Depends(get_database_session)],
        authorize: AuthJWT = Depends(),
        token: HTTPAuthorizationCredentials = Depends(auth_scheme)
):
    await authorize.jwt_required()

    user_id: int = await authorize.get_jwt_subject()

    total = sum([product.price * product.quantity for product in products])
    rest = payment.amount - total

    receipt = await ReceiptRepository(database).create_one(
        user_id=user_id,
        products=products,
        payment=payment,
        total=total,
        rest=rest
    )

    return ReceiptSchema.model_validate(receipt, from_attributes=True)


@logger.catch
@router.get('/receipts', response_model=list[ReceiptSchema])
async def get_receipts(
    database: Annotated[AsyncSession, Depends(get_database_session)],
    authorize: AuthJWT = Depends(),
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
    offset: int = 0,
    limit: Annotated[int | None, Query(le=100)] = 25,
):
    await authorize.jwt_required()
    user_id: int = await authorize.get_jwt_subject()

    receipts = await ReceiptRepository(database).get_all(user_id=user_id, offset=offset, limit=limit)

    return [
        ReceiptSchema.model_validate(receipt, from_attributes=True)
        for receipt in receipts
    ]


@logger.catch
@router.get('/receipts/search', response_model=list[ReceiptSchema])
async def get_search_receipts(
    database: Annotated[AsyncSession, Depends(get_database_session)],
    authorize: AuthJWT = Depends(),
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
    payment_type: Annotated[PaymentType, PaymentType.CASH] = None,
    min_amount: Annotated[int | None, Query(ge=1)] = None,
    max_amount: Annotated[int | None, Query(ge=1)] = None,
    from_date: datetime | None = None,
    to_date: datetime | None = None,
    offset: int = 0,
    limit: Annotated[int | None, Query(le=100)] = 25,
):
    await authorize.jwt_required()
    user_id: int = await authorize.get_jwt_subject()

    receipts = await ReceiptRepository(database).search(
        user_id=user_id,
        payment_type=payment_type,
        min_amount=min_amount,
        max_amount=max_amount,
        from_date=from_date,
        to_date=to_date,
        offset=offset,
        limit=limit
    )

    return [
        ReceiptSchema.model_validate(receipt, from_attributes=True)
        for receipt in receipts
    ]


@logger.catch
@router.get('/receipts/{receipt_id}', response_class=PlainTextResponse)
async def get_receipt(
    receipt_id: int,
    database: Annotated[AsyncSession, Depends(get_database_session)],
    width: Annotated[int, Query(ge=32, le=128)] = 42
):
    receipt = await ReceiptRepository(database).get(receipt_id=receipt_id)
    user = await UserRepository(database).get(user_id=receipt.user_id)

    receipt = ReceiptSchema.model_validate(receipt, from_attributes=True)
    user = UserSchema.model_validate(user, from_attributes=True)

    return generate_text_receipt(
        width=width,
        user_name=user.name,
        receipt=receipt
    )
