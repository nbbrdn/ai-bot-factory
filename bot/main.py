import asyncio
import logging

import config
import handlers
from db import BaseModel, create_async_engine, get_session_maker, proceed_schemas
from loader import bot, dp
from middlewares.register_check import RegisterCheck
from sqlalchemy.engine import URL

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s:%(name)s:%(levelname)s:%(message)s"
)
logger = logging.getLogger(__name__)

logging.getLogger("httpx").setLevel(logging.ERROR)
logging.getLogger("aiogram.dispatcher").setLevel(logging.ERROR)
logging.getLogger("aiogram.event").setLevel(logging.ERROR)


async def on_startup():
    logger.info("Bot started")


async def main():
    dp.message.middleware(RegisterCheck())
    dp.callback_query.middleware(RegisterCheck())
    dp.include_router(handlers.router)
    dp.startup.register(on_startup)

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
    await proceed_schemas(async_engine, BaseModel.metadata)

    await dp.start_polling(bot, skip_updates=True, session_maker=session_maker)


if __name__ == "__main__":
    asyncio.run(main())
