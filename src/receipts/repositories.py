from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.models import Receipt
from src.receipts.schemas import (
    ProductSchema,
    PaymentSchema
)
from src.receipts.enums import PaymentType
from datetime import datetime


class ReceiptRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_one(
            self,
            user_id: int,
            products: list[ProductSchema],
            payment: PaymentSchema,
            total: float,
            rest: float,
    ):
        receipt = Receipt(
            id=None,
            user_id=user_id,
            products=[product.model_dump() for product in products],
            payment=payment.model_dump(),
            total=total,
            rest=rest
        )
        self._session.add(receipt)
        await self._session.flush()
        await self._session.commit()

        return receipt

    async def get(
            self,
            receipt_id: int,
    ) -> Receipt | None:
        statement = select(Receipt).where(Receipt.id == receipt_id)
        result = await self._session.execute(statement)
        return result.scalar_one_or_none()

    async def get_all(
            self,
            user_id: int,
            limit: int,
            offset: int = 0,
    ) -> list[Receipt]:
        statement = select(Receipt).filter(Receipt.user_id == user_id).limit(limit).offset(offset)
        result = await self._session.execute(statement)
        return result.scalars()

    async def search(
            self,
            user_id: int,
            payment_type: PaymentType,
            min_amount: int = None,
            max_amount: int = None,
            from_date: datetime = None,
            to_date: datetime = None,
            limit: int = 10,
            offset: int = 0
    ):
        statement = select(Receipt).filter(Receipt.user_id == user_id)

        if payment_type:
            statement = statement.filter(Receipt.payment['type'] == payment_type)

        if min_amount:
            statement = statement.filter(Receipt.total >= min_amount)
        if max_amount:
            statement = statement.filter(Receipt.total <= max_amount)

        if from_date:
            statement = statement.filter(Receipt.created_at >= from_date)
        if to_date:
            statement = statement.filter(Receipt.created_at <= to_date)

        statement = statement.limit(limit).offset(offset)
        result = await self._session.execute(statement)

        return result.scalars()
