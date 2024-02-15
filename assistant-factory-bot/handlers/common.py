from aiogram import Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message

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
    await message.answer(
        text="Привет!\n\nЯ - бот, который поможет создать тебе "
        "своего собственного Telegram-бота, обладающего возможностями "
        "OpenAI ассистента!\n\n"
        "Для того, чтобы узнать, какие тебе доступны команды, введи команду /help"
    )


@router.message(Command(commands="help"), StateFilter(default_state))
async def proccess_help_command(message: Message) -> None:
    """
    Handles the /help command for the bot.

    Sends a list of the bot commands.

    Args:
        message (Message): The incoming message object.

    Returns:
        None
    """
    await message.answer(
        text="Команды бота:\n\n"
        "/start - активирует бота\n\n"
        "/stop - останавливает бота\n\n"
        "/reg - запускает процесс регистрации пользователя\n\n"
        "/new - запускает процесс создания асисстента\n\n"
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


# Этот хэндлер будет срабатывать на любые сообщения, кроме тех
# для которых есть отдельные хэндлеры, вне состояний
@router.message(StateFilter(default_state))
async def send_echo(message: Message) -> None:
    await message.reply(text="Извините, моя твоя не понимать")
