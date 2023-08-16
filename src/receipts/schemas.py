from pydantic import BaseModel

from datetime import datetime

from src.receipts.enums import PaymentType


class ProductSchema(BaseModel):
    name: str
    price: float
    quantity: int


class PaymentSchema(BaseModel):
    type: PaymentType
    amount: float


class ReceiptSchema(BaseModel):
    id: int
    products: list[ProductSchema]
    payment: PaymentSchema
    total: float
    rest: float
    created_at: datetime
