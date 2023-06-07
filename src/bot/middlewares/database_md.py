from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message

from src.bot.structures import TransferData
from src.db import Database


class DatabaseMiddleware(BaseMiddleware):
    """This middleware throw a Database class to handler"""

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message | CallbackQuery,
            data: TransferData,
    ) -> Any:
        async with data["pool"]() as session:
            data["db"] = Database(session)
            return await handler(event, data)
