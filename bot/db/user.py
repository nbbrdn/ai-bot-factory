import datetime

from sqlalchemy import DATE, VARCHAR, Column, Integer, update
from sqlalchemy.orm import sessionmaker

from .base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    user_id = Column(Integer, unique=True, nullable=False, primary_key=True)
    username = Column(VARCHAR(32))
    ref_id = Column(Integer, nullable=True)
    reg_date = Column(DATE, default=datetime.date.today())
    upd_date = Column(DATE, onupdate=datetime.date.today())
    msg_remain = Column(Integer, default=30)

    def __str__(self):
        return f"<User: {self.user_id}>"


async def update_user_last_activity(user_id: int, session_maker: sessionmaker) -> None:
    async with session_maker() as session:
        async with session.begin():
            stmt = (
                update(User)
                .where(User.user_id == user_id)
                .values(upd_date=datetime.date.today())
            )
            await session.execute(stmt)
            await session.commit()
