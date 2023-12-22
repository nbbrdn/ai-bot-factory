import asyncio
import logging
import os

from aiogram import Bot, Dispatcher

import handlers

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s:%(name)s:%(levelname)s:%(message)s"
)
logger = logging.getLogger(__name__)

logging.getLogger("httpx").setLevel(logging.ERROR)
logging.getLogger("aiogram.dispatcher").setLevel(logging.ERROR)
logging.getLogger("aiogram.event").setLevel(logging.ERROR)

tg_token = os.environ.get("BOT_TOKEN")


async def on_startup():
    logger.info("Bot started")


async def main():
    bot = Bot(token=tg_token)
    dp = Dispatcher()
    dp.include_router(handlers.router)
    dp.startup.register(on_startup)

    await dp.start_polling(
        bot,
        skip_updates=True,
    )


if __name__ == "__main__":
    asyncio.run(main())
