from sqlalchemy import select
from utilities.extensions import db
from database.models.user import User


def create_user(data: dict) -> User:
    user = User(
        username=data["username"],
        email=data["email"],
    )
    db.session.add(user)
    db.session.commit()
    return user


def get_users(limit: int | None):
    stmt = select(User).limit(limit)
    return db.session.scalars(stmt).all()


def get_user(identifier: str | int):
    if isinstance(identifier, int):
        stmt = select(User).where(User.id == identifier)
    elif "@" in identifier:
        stmt = select(User).where(User.email == identifier)
    else:
        stmt = select(User).where(User.username == identifier)

    return db.session.scalar(stmt)
