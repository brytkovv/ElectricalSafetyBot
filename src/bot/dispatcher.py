""" This file contains build dispatcher logic """
from typing import Optional

from aiogram import Bot
from aiogram import Dispatcher
from aiogram.fsm.storage.base import BaseEventIsolation, BaseStorage
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.strategy import FSMStrategy

from src.bot.handlers import routers
from src.bot.middlewares import DatabaseMiddleware, RegisterCheck
from src.cache import Cache
from src.configuration import conf


def get_redis_storage(
        redis: Cache, state_ttl=conf.redis.state_ttl, data_ttl=conf.redis.data_ttl
):
    return RedisStorage(redis=redis, state_ttl=state_ttl, data_ttl=data_ttl)


def get_dispatcher(
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

    # Register middlewares
    dp.message.middleware(DatabaseMiddleware())
    dp.callback_query.middleware(DatabaseMiddleware())

    dp.message.middleware(RegisterCheck())
    dp.callback_query.middleware(RegisterCheck())

    return dp
