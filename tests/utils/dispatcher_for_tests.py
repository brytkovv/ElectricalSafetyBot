from typing import Optional

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.base import BaseStorage, BaseEventIsolation
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.strategy import FSMStrategy

from src.bot.handlers import routers


def get_dispatcher_for_tests(
        storage: BaseStorage = MemoryStorage(),
        fsm_strategy: Optional[FSMStrategy] = FSMStrategy.CHAT,
        event_isolation: Optional[BaseEventIsolation] = None,
        bot: Bot = None
):
    """This function set up dispatcher with routers, filters and middlewares"""
    dp = Dispatcher(
        storage=storage, fsm_strategy=fsm_strategy, events_isolation=event_isolation
    )
    for router in routers:
        dp.include_router(router)

    # Register middlewares # TODO: как нормально протестировать middleware?
    # dp.message.middleware(DatabaseMiddleware())
    # dp.callback_query.middleware(DatabaseMiddleware())
    #
    # dp.message.middleware(RegisterCheck())
    # dp.callback_query.middleware(RegisterCheck())

    return dp
