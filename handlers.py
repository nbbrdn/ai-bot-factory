from aiogram import Router, F, flags
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionMiddleware
from aiogram.enums import ChatAction

import logging
import re

import external

logger = logging.getLogger(__name__)

router = Router()
router.message.middleware(ChatActionMiddleware())

threads = {}


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Тут будут две кнопки")


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

    text = await external.generate_text(prompt, thread_id)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"\*(.+?)\*", r"<i>\1</i>", text)

    await message.answer(text)
    logging.info(f"bot (id={user_id}): {text}")
