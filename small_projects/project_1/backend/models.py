from __future__ import annotations

from datetime import UTC, datetime
from sqlalchemy import DateTime, Integer, String, Text, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from db import Base

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True, 
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(25),
        unique=True,
        nullable=False
    )

    description: Mapped[str] = mapped_column(
        Text,
    )

    category: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    price: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        default=1
    )

    in_stock: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )