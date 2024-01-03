import os
from pprint import pprint

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from openai import OpenAI

# https://t.me/aifabriqbot
BOT_TOKEN = os.environ.get("FABRIQ_BOT_TOKEN")
OPENAI_TOKEN = os.environ.get("OPENAI_TOKEN")

client = OpenAI(api_key=OPENAI_TOKEN)

storage = MemoryStorage()
bot = Bot(BOT_TOKEN)
dp = Dispatcher()


class FSMCreateAssistant(StatesGroup):
    fill_assistant_name = State()
    fill_assistant_instrustion = State()


class FSMDeleteAssistant(StatesGroup):
    enter_assistant_number = State()
    confirm_del_action = State()


# Этот хэндлер будет срабатывать на команду /start вне состояний
# и предлагать перейти к заполнению анкеты, отправив команду /newassistant
@dp.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    await message.answer(
        text="Это бот демонстрирует создание OpenAI ассистентов\n\n"
        "Чтобы перейти к созданию ассистента - "
        "отправьте команду /newassistant"
    )


# Этот хэндлер будет срабатывать на команду "/cancel" в состоянии
# по умолчанию и сообщать, что эта команда работает внутри машины состояний
@dp.message(Command(commands="cancel"), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(
        text="Отменять нечего.\n\n"
        "Чтобы перейти к созданию ассистента - "
        "отправьте команду /newassistant"
    )


# Этот хэндлер будет срабатывать на команду "/cancel" в любых состояниях,
# кроме состояния по умолчанию, и отключать машину состояний
@dp.message(Command(commands="cancel"), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(
        text="Вы вышли из машины состояний\n\n"
        "Чтобы снова перейти к заполнению анкеты - "
        "отправьте команду /newassistant"
    )
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()


# Этот хэндлер будет срабатывать на команду "/test" в состоянии по умолчанию
@dp.message(Command(commands="test"), StateFilter(default_state))
async def process_test_command(message: Message):
    assistant = client.beta.assistants.create(
        name="Test assistant",
        instructions="Ты чат-бот, который любит потравить анекдоты",
        model="gpt-4-1106-preview",
        tools=[{"type": "retrieval"}],
        metadata={"client_id": message.from_user.id},
    )

    pprint(assistant)  # asst_DsOIRbyyqvYVHtBSbSbapwBX

    # my_assistants = client.beta.assistants.list()
    # pprint(my_assistants.data)
    await message.answer(text="test!")


# Этот хэндлер будет срабатывать на команду "/assistants" в состоянии по умолчанию
@dp.message(Command(commands="assistants"), StateFilter(default_state))
async def process_assistants_command(message: Message):
    my_assistants = []
    telegram_user_id = message.from_user.id
    assistants = client.beta.assistants.list()
    data = assistants.data
    for assistant in data:
        metadata = assistant.metadata
        if "client_id" in metadata:
            try:
                client_id = int(metadata["client_id"])
            except ValueError:
                client_id = 0
            if client_id == telegram_user_id:
                my_assistants.append({"id": assistant.id, "name": assistant.name})

    if my_assistants:
        text = ""
        for i, assistant in enumerate(my_assistants, start=1):
            text += f"{i}. {assistant['name']}\n"
        await message.answer(text=text)
    else:
        await message.answer(
            text="У вас нет асисстентов. Чтобы создать, введите команду /newassistant"
        )


# Этот хэндлер будет срабатывать на команду /delassistant, выводить
# список асисстентов пользователя и переводить в состояние ожидания ввода номера
# ассистента для удаления
@dp.message(Command(commands="delassistant"), StateFilter(default_state))
async def process_delassistant_command(message: Message, state: FSMContext):
    my_assistants = []
    telegram_user_id = message.from_user.id
    assistants = client.beta.assistants.list()
    data = assistants.data
    for assistant in data:
        metadata = assistant.metadata
        if "client_id" in metadata:
            try:
                client_id = int(metadata["client_id"])
            except ValueError:
                client_id = 0
            if client_id == telegram_user_id:
                my_assistants.append({"id": assistant.id, "name": assistant.name})

    if my_assistants:
        await state.update_data(assistants=my_assistants)
        text = ""
        for i, assistant in enumerate(my_assistants, start=1):
            text += f"{i}. {assistant['name']}\n"
        await message.answer(text="Вот список ваших асисстентов: ")
        await message.answer(text=text)
        await message.answer("Введите номер ассистента, которого хотите удалить:")
        await state.set_state(FSMDeleteAssistant.enter_assistant_number)
    else:
        await message.answer(
            text="У вас нет асисстентов. Чтобы создать, введите команду /newassistant"
        )
        await state.clear()


# Это хэндлер будет срабатывать, если введен корректный номер ассистента
# и запрашивать подтверждение на его удаление
@dp.message(
    StateFilter(FSMDeleteAssistant.enter_assistant_number),
    lambda x: x.text.isdigit() and int(x.text) >= 0,
)
async def process_assistant_number_sent(message: Message, state: FSMContext):
    assistant_idx = int(message.text) - 1
    data = await state.get_data()
    assistants = data["assistants"]
    if len(assistants) <= assistant_idx:
        await message.answer(text="Ассистента с указанным номером не существует.")
    else:
        assistant = assistants[assistant_idx]
        await state.update_data(assistant_id_to_delete=assistant["id"])

        yes_button = InlineKeyboardButton(text="Да", callback_data="yes")
        no_button = InlineKeyboardButton(text="Нет", callback_data="no")
        keyboard: list[list[InlineKeyboardButton]] = [[yes_button, no_button]]
        markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
        await message.answer(
            text=f"Вы действительно хотите удалить ассистента \"{assistant['name']}\"?",
            reply_markup=markup,
        )

        await state.set_state(FSMDeleteAssistant.confirm_del_action)


# Это хэндлер будет срабатывать на подтверждение удаления ассистента
# и выводить из машины состояний
@dp.callback_query(
    StateFilter(FSMDeleteAssistant.confirm_del_action), F.data.in_(["yes", "no"])
)
async def process_assistant_delete_confirm_press(
    callback: CallbackQuery, state: FSMContext
):
    if callback.data == "yes":
        data = await state.get_data()
        assistant_id = data["assistant_id_to_delete"]
        client.beta.assistants.delete(assistant_id=assistant_id)
        await callback.message.edit_text(text="Асисстент успешно удален!")
    else:
        await callback.message.edit_text(text="Удаление ассистента отменено!")
    await state.clear()


# Этот хэнтдер будет срабатывать на команду /newassistant
# и переводить в состояние ожидания ввода имени ассистента
@dp.message(
    Command(commands="newassistant"),
    StateFilter(default_state),
)
async def process_newassistant_command(message: Message, state: FSMContext):
    await message.answer(text="Пожалуйста введите имя ассистента")
    # Устанавливаем состояние ожидание ввода названия ассистента
    await state.set_state(FSMCreateAssistant.fill_assistant_name)


# Этот хэндлер будет срабатывать, если введено корректное имя
# и переводить в состояние ожидания ввода инструкции
@dp.message(StateFilter(FSMCreateAssistant.fill_assistant_name))
async def process_assistant_name_sent(message: Message, state: FSMContext):
    # Сохраняем введенное имя в хранилище по ключу "assistant_name"
    await state.update_data(assistant_name=message.text)
    await message.answer(
        text="Спасибо!\n\n А теперь введите текст инструкции для ассистента"
    )
    # Устанавливаем состояние ожидания ввода инструкции
    await state.set_state(FSMCreateAssistant.fill_assistant_instrustion)


# Этот хэндлер будет срабатывать, если введена корректная инструкция
# и выводить из машины состояний
@dp.message(StateFilter(FSMCreateAssistant.fill_assistant_instrustion))
async def process_assistant_instruction_sent(message: Message, state: FSMContext):
    # Сохраняем инструкцию в хранилище по ключу "assistant_instruction"
    await state.update_data(assistant_instruction=message.text)

    # Завершаем машину состояний
    await state.clear()
    # Отправляем в чат сообщение о завершении процесса
    await message.answer(text="Спасибо! Ваш ассистен создан!")


# Этот хэндлер будет срабатывать на любые сообщения, кроме тех
# для которых есть отдельные хэндлеры, вне состояний
@dp.message(StateFilter(default_state))
async def send_echo(message: Message):
    await message.reply(text="Извините, моя твоя не понимать")


if __name__ == "__main__":
    dp.run_polling(bot)
