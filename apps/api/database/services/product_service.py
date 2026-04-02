import sqlalchemy.exc
from sqlalchemy.orm import selectinload

from database.exceptions import handle_error
from database.src.base import db
from database.src.models.product import Product, ProductDetails


def create_product(data: dict) -> Product:
    try:
        product = Product(name=data["name"])
        product.details = ProductDetails(price=data["price"])
        db.session.add(product)
        db.session.commit()
    except (sqlalchemy.exc.IntegrityError, sqlalchemy.exc.OperationalError) as e:
        db.session.rollback()
        handle_error(e)
    else:
        return product


def get_products(limit: int | None):
    stmt = (
        sqlalchemy.select(Product)
        .options(selectinload(Product.details))
        .limit(limit)
    )
    return db.session.scalars(stmt).all()


def get_product(identifier: str | int):
    stmt = sqlalchemy.select(Product).options(selectinload(Product.details))

    if isinstance(identifier, int):
        stmt = stmt.where(Product.id == identifier)
    else:
        stmt = stmt.where(Product.name == identifier)

    return db.session.scalar(stmt)
