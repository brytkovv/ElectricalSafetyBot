from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from redis.asyncio.client import Redis

from src.db import Database


class RegisterCheck(BaseMiddleware):  # TODO: переделать в фильтр?
    """
    Middleware будет вызываться каждый раз, когда пользователь будет отправлять боту сообщения (или нажимать
    на кнопку в инлайн-клавиатуре).
    """

    def __init__(self):
        """
        Не нужен в нашем случае
        """
        pass

    @staticmethod
    async def is_user_exists(user, cache, db) -> bool:
        res = await cache.get(key='is_id_exists:' + str(user.id))
        if not res:
            result = await db.user.get(user.id)
            await cache.set(key='is_id_exists:' + str(user.id),
                            value=1 if result else 0)
            return bool(result)
        else:
            return bool(res)

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message | CallbackQuery,
            data: Dict[str, Any]
    ) -> Any:
        """ Сама функция для обработки вызова """
        user = event.from_user
        db = data["db"]
        db: Database
        cache = data["cache"]
        cache: Redis

        check_user = await self.is_user_exists(user, cache, db)
        if not check_user:
            await db.user.new(user_id=user.id,
                              user_name=user.first_name
                              )
            await db.test.new(user_id=user.id)
            await data['bot'].send_message(user.id, 'Ты успешно зарегистрирован(а)!')
            await db.session.commit()
        return await handler(event, data)
