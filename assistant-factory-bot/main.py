import asyncio
import logging

from handlers.common import router as common_router
from handlers.users import router as users_router
from handlers.assistants import router as assistants_router
from loader import bot, dp

from sqlalchemy.engine import URL
import config
from db import BaseModel, create_async_engine, get_session_maker, proceed_schemas

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s:%(name)s:%(levelname)s:%(message)s"
)
logger = logging.getLogger("assistant-factory-bot")


async def on_startup():
    logger.info("Bot started successfully.")


async def main():
    dp.include_routers(common_router, users_router, assistants_router)
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
