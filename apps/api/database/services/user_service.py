# import sqlalchemy
from database.exceptions import handle_error
import sqlalchemy.exc
from database.src.base import db
from database.src.models.user import User


# TODO dict unpacking that automatically uses variables and leaves extras for both product and product_details
def create_user(data: dict) -> User:
    try:
        user = User(
            **data,
        )
        db.session.add(user)
        db.session.commit()
    except (sqlalchemy.exc.IntegrityError, sqlalchemy.exc.OperationalError, TypeError) as e:
        db.session.rollback()
        print("error:", e)
        handle_error(e)
    else:
        return user


def get_users(limit: int | None):
    stmt = sqlalchemy.select(User).limit(limit)
    return db.session.scalars(stmt).all()


def get_user(identifier: str | int):
    if isinstance(identifier, int):
        stmt = sqlalchemy.select(User).where(User.id == identifier)
    elif "@" in identifier:
        stmt = sqlalchemy.select(User).where(User.email == identifier)
    else:
        stmt = sqlalchemy.select(User).where(User.username == identifier)

    return db.session.scalar(stmt)
