from typing import TYPE_CHECKING
from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text, Numeric, ForeignKey

from ..models.base import Model

if TYPE_CHECKING:
    from .category import Category


class Product(Model):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, init=False)
    name: Mapped[str] = mapped_column(String(100), index=True)

    details: Mapped["ProductDetails"] = relationship(
        back_populates="product",
        cascade="all, delete-orphan",
        uselist=False,
        init=False,
    )

    categories: Mapped[list[Category]] = relationship(
        secondary="product_category",
        back_populates="products",
        init=False,
    )


class ProductDetails(Model):
    __tablename__ = "product_details"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, init=False)
    product_id: Mapped[int] = mapped_column(
        ForeignKey("product.id", ondelete="CASCADE"),
        nullable=False,
        init=False,
    )

    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    description: Mapped[str] = mapped_column(Text, default="")

    product: Mapped[Product] = relationship(back_populates="details", init=False)