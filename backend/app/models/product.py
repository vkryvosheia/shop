from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.category import Category


class Product(Base):
    __tablename__ = "products"

    __table_args__ = (
        CheckConstraint("price > 0", name="price_positive"),
        CheckConstraint("stock >= 0", name="stock_non_negative"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    slug: Mapped[str] = mapped_column(String(220), unique=True, nullable=False)
    short_description: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    stock: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0", default=0)
    sku: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    is_visible: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("0"), default=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=text("now()"), nullable=False, index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=text("now()"), onupdate=text("now()"), nullable=False
    )

    category: Mapped[Category] = relationship("Category", back_populates="products")
