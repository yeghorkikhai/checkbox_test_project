from pydantic import BaseModel, Field

from datetime import datetime

from src.receipts.enums import PaymentType


class ProductSchema(BaseModel):
    name: str = Field(min_length=1, max_length=64)

    price: int = Field(ge=1)
    """Product price in minimum units"""

    quantity: int = Field(ge=1)


class PaymentSchema(BaseModel):
    type: PaymentType
    amount: int = Field(ge=1)
    """Payment amount in minimum units"""


class ReceiptSchema(BaseModel):
    id: int
    products: list[ProductSchema] = Field(min_items=1)
    payment: PaymentSchema

    total: int = Field(ge=1)
    """Total amount in minimum units"""

    rest: int = Field(ge=0)
    """Rest of amount in minimum units"""

    created_at: datetime
