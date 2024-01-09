import asyncio
import logging

from handlers.common import router as common_router
from handlers.register_user import router as register_user_router
from loader import bot, dp

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s:%(name)s:%(levelname)s:%(message)s"
)
logger = logging.getLogger("assistant-factory-bot")


async def on_startup():
    logger.info("Bot started successfully.")


async def main():
    dp.include_routers(common_router, register_user_router)
    dp.startup.register(on_startup)
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
