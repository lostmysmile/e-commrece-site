from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey

from database.build.base import Model

class User(Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, init=False)
    username: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(120), unique=True)

    password: Mapped["Password"] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        uselist=False,
        init=False,
    )


class Password(Model):
    __tablename__ = "password"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, init=False)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        init=False,
    )

    hash: Mapped[str] = mapped_column(String(128))
    salt: Mapped[str] = mapped_column(String(32))

    user: Mapped["User"] = relationship(back_populates="password", init=False)