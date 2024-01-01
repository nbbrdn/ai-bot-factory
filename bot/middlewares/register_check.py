from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message
from db import User, update_user_last_activity
from sqlalchemy import select
from sqlalchemy.engine import ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker


class RegisterCheck(BaseMiddleware):
    def __init__(self):
        pass

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        session_maker: sessionmaker = data["session_maker"]
        async with session_maker() as session:
            async with session.begin():
                session: AsyncSession
                result: ScalarResult = await session.execute(
                    select(User).where(User.user_id == event.from_user.id)
                )
                user: User = result.one_or_none()

                if user is None:
                    user = User(
                        user_id=event.from_user.id, username=event.from_user.username
                    )
                    await session.merge(user)
                else:
                    await update_user_last_activity(event.from_user.id, session_maker)
        return await handler(event, data)
