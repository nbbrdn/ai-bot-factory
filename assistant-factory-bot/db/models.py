from sqlalchemy import VARCHAR, BigInteger, Column, ForeignKey, Integer, Boolean

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


class Project(BaseModel, Model):
    __tablename__ = "factory_projects"

    id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey("factory_users.id"), nullable=False)
    comment = Column(VARCHAR(250))
    assistant_id = Column(VARCHAR(250))
    file_id = Column(VARCHAR(250))


class Assistant(BaseModel, Model):
    __tablename__ = "factory_assistants"

    id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey("factory_users.id"), nullable=False)
    assistant_id = Column(VARCHAR(250))
    name = Column(VARCHAR(250))

    def __init__(self, owner_id, assistant_id, name):
        self.owner_id = owner_id
        self.assistant_id = assistant_id
        self.name = name
