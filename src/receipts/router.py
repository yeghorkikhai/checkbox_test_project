from fastapi import APIRouter

from datetime import datetime

from src.receipts.enums import PaymentType
from src.receipts.schemas import (
    ProductSchema,
    PaymentSchema,
    ReceiptSchema
)

router = APIRouter()


@router.post('/receipts', response_model=ReceiptSchema)
async def create_receipt(products: list[ProductSchema], payment: PaymentSchema):
    ...


@router.get('/receipts', response_model=list[ReceiptSchema])
async def get_receipts(
    payment_type: PaymentType,
    min_amount: float,
    max_amount: float,
    from_date: datetime,
    to_date: datetime,
    offset: int,
    limit: int
):
    ...


@router.get('/receipts/{receipt_id}', response_model=str)
async def get_receipt(receipt_id: str):
    ...
