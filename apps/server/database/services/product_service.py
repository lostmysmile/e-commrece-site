from sqlalchemy import select
from sqlalchemy.orm import selectinload

from database.build.base import db
from database.build.models.product import Product, ProductDetails

def create_product(data: dict) -> Product:
    product = Product(name=data["name"])
    product.details = ProductDetails(price=data["price"])
    db.session.add(product)
    db.session.commit()
    return product


def get_products(limit: int | None):
    stmt = (
        select(Product)
        .options(selectinload(Product.details))
        .limit(limit)
    )
    return db.session.scalars(stmt).all()


def get_product(identifier: str | int):
    stmt = select(Product).options(selectinload(Product.details))

    if isinstance(identifier, int):
        stmt = stmt.where(Product.id == identifier)
    else:
        stmt = stmt.where(Product.name == identifier)

    return db.session.scalar(stmt)