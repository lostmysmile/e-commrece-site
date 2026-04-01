
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey
from database.build.base import Model

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .product import Product


class ProductCategory(Model):
    __tablename__ = "product_category"

    product_id: Mapped[int] = mapped_column(
        ForeignKey("product.id"), primary_key=True, init=False
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey("category.id"), primary_key=True, init=False
    )


class Category(Model):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, init=False)
    name: Mapped[str] = mapped_column(String(50), unique=True, index=True)

    products: Mapped[list[Product]] = relationship(
        secondary="product_category",
        back_populates="categories",
        init=False,
    )
