from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import Message

from aiogram.fsm.context import FSMContext

from db.orm import get_msg_cnt, is_admin, user_exists, add_credits
from states import FSMCreditUser

router = Router()


@router.message(Command(commands="balance"), StateFilter(default_state))
async def process_balance_command(message: Message) -> None:
    telegram_user_id = message.from_user.id
    cnt = await get_msg_cnt(telegram_user_id)
    await message.answer(text=f"Ваш баланс: {cnt} сообщений.")


@router.message(Command(commands="credit"), StateFilter(default_state))
async def process_credit_command(message: Message, state: FSMContext) -> None:
    telegram_user_id = message.from_user.id
    is_user_admin = await is_admin(telegram_user_id)
    if not is_user_admin:
        await message.answer(
            text="У вас недостаточно прав на зачисление кредитов пользователям."
        )
        await state.clear()
        return

    await message.answer(
        text="Вы собираетесь пополнить баланс запросов к ChatGPT для пользователя Telegram. Введите ID пользователя:"
    )
    await state.set_state(FSMCreditUser.enter_user_id)


@router.message(StateFilter(FSMCreditUser.enter_user_id))
async def process_entered_user_id(message: Message, state: FSMContext) -> None:
    user_id = message.text
    found = await user_exists(user_id)
    if not found:
        await message.answer(
            text=f"Пользователь с ID {user_id} в списке пользователей бота не найден."
        )
        await state.clear()
        return

    await state.update_data(credit_user_id=user_id)
    await message.answer(
        text=f"Введите сумму кредитов, которые будут начислены пользователю с id: {user_id}"
    )
    await state.set_state(FSMCreditUser.enter_credit)


@router.message(StateFilter(FSMCreditUser.enter_credit))
async def process_entered_credit(message: Message, state: FSMContext) -> None:
    try:
        credits = int(message.text)
    except ValueError as ex:
        await message.answer(text=f"{message.text} не является целым числом.")
        return
    data = await state.get_data()
    credit_user_id = data.get("credit_user_id")
    await add_credits(credit_user_id, credits)
    await message.answer(
        text=f"Баланс пользователя {credit_user_id} пополнен на {credits} кредитов."
    )
    await state.clear()
