import config
from db import create_async_engine, get_session_maker
from db.models import Dialog
from db.user import User
from sqlalchemy import select, update
from sqlalchemy.engine import URL, ScalarResult

postgres_url = URL.create(
    "postgresql+asyncpg",
    username=config.POSTGRES_USER,
    password=config.POSTGRES_PASSWORD,
    host="db",
    port=5432,
    database=config.POSTGRES_DB,
)

async_engine = create_async_engine(postgres_url)
session_maker = get_session_maker(async_engine)


async def has_referrer(user_id: int) -> bool:
    async with session_maker() as session:
        async with session.begin():
            stmt = select(User).where(User.ref_id == user_id)
            result: ScalarResult = await session.execute(stmt)
            referrers = result.all()
            if len(referrers) == 0:
                return False
            return True


async def is_registered(user_id: int) -> bool:
    async with session_maker() as session:
        async with session.begin():
            stmt = select(User).where(User.user_id == user_id)
            result: ScalarResult = await session.execute(stmt)
            users = result.all()
            if len(users) == 0:
                return False
            return True


async def update_referrer(user_id: int, referrer_id: int):
    async with session_maker() as session:
        async with session.begin():
            stmt = (
                update(User).where(User.user_id == user_id).values(ref_id=referrer_id)
            )
            await session.execute(stmt)
            await session.commit()


async def count_referrals(user_id: int) -> int:
    async with session_maker() as session:
        async with session.begin():
            stmt = select(User).where(User.ref_id == user_id)
            result: ScalarResult = await session.execute(stmt)
            referrals = result.all()

            return len(referrals)


async def count_users() -> int:
    async with session_maker() as session:
        async with session.begin():
            stmt = select(User)
            result: ScalarResult = await session.execute(stmt)
            users = result.all()

            return len(users)


async def save_message(user_id: int, msg: str, user_msg: bool = True):
    async with session_maker() as session:
        async with session.begin():
            if user_msg:
                actor = "user"
            else:
                actor = "gpt"
            dialog = Dialog(user_id=user_id, actor=actor, msg=msg)
            await session.merge(dialog)


async def update_msg_cnt(user_id: int, remain: int):
    if remain > 0:
        remain -= 1
    async with session_maker() as session:
        async with session.begin():
            stmt = update(User).where(User.user_id == user_id).values(msg_remain=remain)
            await session.execute(stmt)
            await session.commit()


async def get_msg_cnt(user_id: int):
    async with session_maker() as session:
        async with session.begin():
            stmt = select(User).where(User.user_id == user_id)
            result: ScalarResult = await session.execute(stmt)
            user = result.first()
            print(user)
            return user.msg_remain
