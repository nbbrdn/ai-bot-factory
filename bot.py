import asyncio
import logging
import os

from aiogram import Bot, Dispatcher

import handlers

logging.basicConfig(level=logging.INFO, filename="bot.log")
tg_token = os.environ.get("BOT_TOKEN")


async def on_startup():
    logging.info("bot started")


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
