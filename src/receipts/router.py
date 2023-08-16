from typing import Annotated

from fastapi import APIRouter, Depends

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from fastapi.responses import PlainTextResponse

from async_fastapi_jwt_auth import AuthJWT

from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies import get_database_session

from .repositories import ReceiptRepository

from src.receipts.enums import PaymentType
from src.receipts.schemas import (
    ProductSchema,
    PaymentSchema,
    ReceiptSchema
)
from .utils import generate_text_receipt

router = APIRouter()

auth_scheme = HTTPBearer()


@router.post('/receipts', response_model=ReceiptSchema)
async def create_receipt(
        products: list[ProductSchema],
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


@router.get('/receipts', response_model=list[ReceiptSchema])
async def get_receipts(
    offset: int,
    limit: int,
    database: Annotated[AsyncSession, Depends(get_database_session)],
    authorize: AuthJWT = Depends(),
    token: HTTPAuthorizationCredentials = Depends(auth_scheme)
):
    await authorize.jwt_required()
    user_id: int = await authorize.get_jwt_subject()

    receipts = await ReceiptRepository(database).get_all(user_id=user_id, offset=offset, limit=limit)

    return [
        ReceiptSchema.model_validate(receipt, from_attributes=True)
        for receipt in receipts
    ]


@router.get('/receipts/search', response_model=list[ReceiptSchema])
async def get_search_receipts(
    database: Annotated[AsyncSession, Depends(get_database_session)],
    authorize: AuthJWT = Depends(),
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
    payment_type: PaymentType | None = None,
    min_amount: float | None = None,
    max_amount: float | None = None,
    from_date: datetime | None = None,
    to_date: datetime | None = None,
    offset: int = 0,
    limit: int = 10,
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


@router.get('/receipts/{receipt_id}', response_class=PlainTextResponse)
async def get_receipt(
    receipt_id: int,
    database: Annotated[AsyncSession, Depends(get_database_session)],
    width: int = 42
):
    receipt = await ReceiptRepository(database).get(receipt_id=receipt_id)
    receipt = ReceiptSchema.model_validate(receipt, from_attributes=True)

    return generate_text_receipt(
        width=width,
        user_name='ФОП Джонсонюк Борис',
        receipt=receipt
    )
