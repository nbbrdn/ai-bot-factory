from database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    message_date = Column(DateTime)
    telegram_user_id = Column(Integer, ForeignKey("telegram_users.id"))
    message_text = Column(Text)


class TelegramUser(Base):
    __tablename__ = "telegram_users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True)
    name = Column(String)
