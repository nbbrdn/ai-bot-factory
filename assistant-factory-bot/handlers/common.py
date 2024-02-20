from aiogram import Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message

from db.orm import user_exists, add_user

router = Router()


@router.message(
    CommandStart(),
    StateFilter(default_state),
)
async def proccess_start_command(message: Message) -> None:
    """
    Handles the /start command for the Telegram bot.

    Sends a welcome message introducing the basic bot commands.

    Args:
        message (Message): The incoming message object.

    Returns:
        None
    """

    exists = await user_exists(message.from_user.id)
    if not exists:
        id = message.from_user.id
        username = message.from_user.username
        print(id, username)
        await add_user(id, username)

    await message.answer(
        text="Привет!\n\nЯ - бот, который поможет создать тебе "
        "своего собственного Telegram-бота, обладающего возможностями "
        "OpenAI ассистента!\n\n"
        "Для того, чтобы узнать, какие тебе доступны команды, введи команду /help"
    )


@router.message(Command(commands="cancel"), StateFilter(default_state))
async def process_cancel_command(message: Message) -> None:
    """
    Handles the /cancel command for the bot.

    Sends a message indicating that there's nothing to cancel and provides guidance on
    creating an assistant.

    Args:
        message (Message): The incoming message object.

    Returns:
        None
    """
    await message.answer(
        text="Отменять нечего.\n\n"
        "Чтобы перейти к созданию AI бота - "
        "отправьте команду /new"
    )


@router.message(Command(commands="cancel"), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext) -> None:
    """
    Handles the /cancel command when the bot is in a non-default state.

    Notifies the user about exiting the state machine and provides guidance on starting
    over.

    Args:
        message (Message): The incoming message object.
        state (FSMContext): The current state of the finite state machine.

    Returns:
        None
    """
    await message.answer(
        text="Вы вышли из диалога создания AI бота\n\n"
        "Чтобы начать заново - отправьте команду /new"
    )

    await state.clear()
