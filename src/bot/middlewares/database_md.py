from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message

from src.bot.structures import TransferData
from src.cache import Cache
from src.db import Database, create_session_maker


class DatabaseMiddleware(BaseMiddleware):
    """This middleware throw a Database class to handler"""

    # TODO Переделать на функции он процесс/пост
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message | CallbackQuery,
            data: TransferData,
    ) -> Any:
        pool = data.get('pool')  # TODO: костыль для тестов, как занести это в мокед дп
        if not pool:
            data = TransferData(pool=await create_session_maker(), cache=Cache())

        async with data["pool"]() as session:
            data["db"] = Database(session)
            return await handler(event, data)
