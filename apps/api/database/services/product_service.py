import sqlalchemy.exc
from sqlalchemy.orm import selectinload

from database.exceptions import handle_error
from database.src.base import db
from database.src.models.product import Product, ProductDetails
from database.src.models.category import Category


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


def format_product(product: Product):
    return {
        "id": product.id,
        "name": product.name,
        "details": product.details,
        "categories": product.categories,
    }


def get_products(limit: int | None):
    stmt = (
        sqlalchemy.select(Product)
        .options(selectinload(Product.details), selectinload(Product.categories))
        .limit(limit)
    )
    products = db.session.scalars(stmt).all()
    return [format_product(p) for p in products]


def get_categories(limit: int | None):
    stmt = sqlalchemy.select(Category).limit(limit)
    categories = db.session.scalars(stmt).all()
    return [{"id": c.id, "name": c.name} for c in categories]


def get_product(identifier: str | int):
    stmt = sqlalchemy.select(Product).options(selectinload(
        Product.details), selectinload(Product.categories))

    if isinstance(identifier, int):
        stmt = stmt.where(Product.id == identifier)
    else:
        stmt = stmt.where(Product.name == identifier)

    product = db.session.scalar(stmt)
    if not product:
        return None

    return format_product(product)
