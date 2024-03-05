import config
from db.engine import create_async_engine, get_session_maker

from sqlalchemy import select, update
from sqlalchemy.engine import URL, ScalarResult

from .models import User, Assistant

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


async def get_msg_cnt(user_id: int):
    async with session_maker() as session:
        async with session.begin():
            stmt = select(User.msg_remain).where(User.tg_user_id == user_id)
            result: ScalarResult = await session.execute(stmt)
            remain = result.first()
            if remain and remain[0]:
                return remain[0]
            return 0


async def decrease_msg_remain(user_id: int):
    async with session_maker() as session:
        async with session.begin():
            stmt = (
                update(User)
                .where(User.tg_user_id == user_id)
                .values(msg_remain=User.msg_remain - 1)
            )
            await session.execute(stmt)
            await session.commit()


async def is_admin(user_id: int) -> bool:
    async with session_maker() as session:
        async with session.begin():
            stmt = select(User).where(User.tg_user_id == user_id)
            result = await session.execute(stmt)
            user = result.scalar()
            return user is not None and user.is_admin


async def user_exists(user_id: int) -> bool:
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(
                select(User).where(User.tg_user_id == user_id)
            )
            user = result.scalar()
            return user is not None


async def add_credits(user_id: int, credits: int):
    async with session_maker() as session:
        async with session.begin():
            stmt = (
                update(User)
                .where(User.tg_user_id == user_id)
                .values(msg_remain=User.msg_remain + credits)
            )
            await session.execute(stmt)
            await session.commit()


async def add_user(user_id: int, username: str = None):
    async with session_maker() as session:
        async with session.begin():
            new_user = User(tg_user_id=user_id, tg_username=username)
            session.add(new_user)
            await session.commit()
            return new_user


async def add_assistant(tg_user_id: int, assistant_id: str, assistant_name: str = None):
    async with session_maker() as session:
        async with session.begin():
            user = session.query(User).filter_by(tg_user_id=tg_user_id).first()

            if user:
                new_assistant = Assistant(
                    owner_id=user.id, assistant_id=assistant_id, name=assistant_name
                )
                session.add(new_assistant)
            else:
                print(f"Пользователь с tg_user_id {tg_user_id} не найден.")


async def get_assistant_by_id(assistant_id: str):
    async with session_maker() as session:
        async with session.begin():
            assistant = (
                session.query(Assistant).filter_by(assistant_id=assistant_id).first()
            )

            return assistant


async def get_assistants_by_user_id(user_id: int):
    async with session_maker() as session:
        async with session.begin():
            assistents = session.query(Assistant).filter_by(owner_id=user_id).all()

            return assistents
