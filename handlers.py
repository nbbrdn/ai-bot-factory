import logging
import re

from aiogram import F, Router, flags
from aiogram.enums import ChatAction
from aiogram.filters import Command
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from aiogram.utils.chat_action import ChatActionMiddleware

import external

logger = logging.getLogger(__name__)

router = Router()
router.message.middleware(ChatActionMiddleware())

threads = {}


@router.message(Command("start"))
async def cmd_start(message: Message):
    kb = [
        [KeyboardButton(text="Давай разберем случайный кейс")],
        [KeyboardButton(text="Предложи список из 10 случайных кейсов")],
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Укажите способ выбора кейса",
    )

    await message.answer(
        ("Вы хотите выбрать кейс из предложенного списка, или выбрать случайный?"),
        reply_markup=keyboard,
    )


@router.message(F.text)
@flags.chat_action(ChatAction.TYPING)
async def message_with_text(message: Message):
    user_id = message.from_user.id
    thread_id = threads.get(user_id, None)

    if not thread_id:
        thread_id = await external.create_thread()
        threads[user_id] = thread_id

    prompt = message.text
    logging.info(f"user (id={user_id}): {prompt}")
    message = await message.answer("💬", reply_markup=ReplyKeyboardRemove())

    text = await external.generate_text(prompt, thread_id)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"\*(.+?)\*", r"<i>\1</i>", text)

    await message.delete()

    await message.answer(text)
    logging.info(f"bot (id={user_id}): {text}")
