import os

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from openai import OpenAI

from db.orm import add_assistant, get_assistant_by_id, is_admin
from config import logging

OPENAI_TOKEN = os.environ.get("OPENAI_TOKEN")

router = Router()
client = OpenAI(api_key=OPENAI_TOKEN)


@router.message(Command("init"))
async def process_init_command(message: Message) -> None:
    telegram_user_id = message.from_user.id
    is_user_admin = await is_admin(telegram_user_id)
    if not is_user_admin:
        await message.answer(
            text="У вас недостаточно прав для выполнения этой комманды."
        )
        return

    last_assistant_id = None

    while True:
        result = client.beta.assistants.list(limit=100, after=last_assistant_id)
        assistants = result.data

        if not assistants:
            break

        for assistant in assistants:
            metadata = assistant.metadata
            if "client_id" in metadata:
                try:
                    tg_user_id = int(metadata["client_id"])
                    assistant_id = assistant.id
                    assistant_name = assistant.name

                    db_assistant = await get_assistant_by_id(assistant_id)
                    if not (db_assistant):
                        logging.info(
                            f"add assistant: {tg_user_id}, {assistant_id}, {assistant_name}"
                        )
                        add_assistant(tg_user_id, assistant_id, assistant_name)

                except ValueError:
                    await message.answer(
                        text=f"Ассистент {assistant.id}: client_id не найден"
                    )

            last_assistant_id = assistant.id

    await message.answer(text=f"Ассистенты успешно загружены в базу данных.")
