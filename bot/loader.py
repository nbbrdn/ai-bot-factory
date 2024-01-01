import config
from aiogram import Bot, Dispatcher

bot = Bot(token=config.TELEGRAM_BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher()
