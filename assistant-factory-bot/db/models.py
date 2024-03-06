from typing import List
from sqlalchemy import VARCHAR, BigInteger, Column, ForeignKey, Integer, Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel, Model


class User(BaseModel, Model):
    __tablename__ = "factory_users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tg_user_id = Column(BigInteger, unique=True, nullable=False)
    tg_username = Column(VARCHAR(32))
    phone = Column(VARCHAR(11))
    email = Column(VARCHAR(32))
    is_admin = Column(Boolean, default=False)
    msg_remain = Column(Integer, default=0)
    comment = Column(VARCHAR(250))

    assistants: Mapped[List["Assistant"]] = relationship(back_populates="user")


class Assistant(BaseModel, Model):
    __tablename__ = "factory_assistants"

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("factory_users.id"))
    assistant_id: Mapped[str] = mapped_column(String(250))
    name: Mapped[str] = mapped_column(String(250))

    user: Mapped["User"] = relationship(back_populates="assistants")

    def __repr__(self) -> str:
        return (
            f"Assistant("
            f"id={self.id!r}, "
            f"owner_id={self.owner_id!r}, "
            f"assistant_id={self.assistant_id!r}, "
            f"name={self.name!r}"
            f")"
        )
