from sqlalchemy import VARCHAR, BigInteger, Column, ForeignKey, Integer

from .base import Base, Model


class User(Base, Model):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    tg_user_id = Column(BigInteger, unique=True, nullable=False)
    tg_username = Column(VARCHAR(32))
    phone = Column(VARCHAR(11))
    email = Column(VARCHAR(32))
    comment = Column(VARCHAR(250))


class Project(Base, Model):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    comment = Column(VARCHAR(250))
    assistant_id = Column(VARCHAR(250))
    file_id = Column(VARCHAR(250))
