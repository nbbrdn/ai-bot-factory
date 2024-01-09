import asyncio
import logging

import handlers
from loader import bot, dp

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s:%(name)s:%(levelname)s:%(message)s"
)
logger = logging.getLogger("assistant-factory-bot")


async def on_startup():
    logger.info("Bot started successfully.")


async def main():
    dp.include_router(handlers.dp)
    dp.startup.register(on_startup)
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
