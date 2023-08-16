from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column
)

from sqlalchemy.dialects.postgresql import (
    BIGINT,
    VARCHAR,
    JSONB,
    INTEGER,
    TIMESTAMP
)

from datetime import datetime

from src.receipts.schemas import (
    ProductSchema,
    PaymentSchema
)


class Base(DeclarativeBase):
    ...


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)

    name: Mapped[str] = mapped_column(VARCHAR(64), nullable=False)
    login: Mapped[str] = mapped_column(VARCHAR(32), nullable=False)
    password: Mapped[str] = mapped_column(VARCHAR(256), nullable=False)


class Receipt(Base):
    __tablename__ = 'receipts'

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)

    user_id: Mapped[int] = mapped_column(BIGINT, nullable=False)

    products: Mapped[list[ProductSchema]] = mapped_column(JSONB, nullable=False)
    payment: Mapped[PaymentSchema] = mapped_column(JSONB, nullable=False)

    total: Mapped[int] = mapped_column(INTEGER, nullable=False)
    rest: Mapped[int] = mapped_column(INTEGER, nullable=False)

    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, default=datetime.utcnow)
