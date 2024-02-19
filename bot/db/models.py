import datetime

from sqlalchemy import TEXT, VARCHAR, Column, DateTime, Integer

from .base import BaseModel


class Dialog(BaseModel):
    __tablename__ = "negotiator_dialogs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    actor = Column(VARCHAR(4), nullable=False, default="user")
    msg = Column(TEXT)
    created_at = Column(DateTime, default=datetime.datetime.now())
