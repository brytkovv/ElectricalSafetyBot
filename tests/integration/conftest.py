from typing import Callable

import pytest
import pytest_asyncio
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from aiogram.fsm.storage.memory import MemoryStorage
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.structures.data_structure import TransferData
from src.cache import Cache
from src.db.database import create_session_maker
from tests.utils.dispatcher_for_tests import get_dispatcher_for_tests
from tests.utils.fake_data_for_db import dp_filler
from tests.utils.mocked_bot import MockedBot
from tests.utils.mocked_database import MockedDatabase
from tests.utils.mocked_redis import MockedRedis
from tests.utils.updates import TEST_USER, TEST_CHAT


@pytest_asyncio.fixture(scope='session')
async def pool():
    pool_ = await create_session_maker()
    yield pool_
    pool_.close_all()


@pytest_asyncio.fixture(scope='session')
async def db(pool: Callable[[], AsyncSession]):
    session = pool()
    database = MockedDatabase(session)

    await dp_filler(database)
    yield database

    # await database.teardown()
    await session.close()


@pytest.fixture(scope='session')
def bot():
    return MockedBot()


@pytest.fixture(scope='session')
def storage():
    return MemoryStorage()


@pytest.fixture(scope='session')
def dp(storage, db):
    return get_dispatcher_for_tests(storage=storage, db=db)


@pytest.fixture(scope='session')
def cache():
    return Cache(redis=MockedRedis())


@pytest.fixture(scope='session')
def transfer_data(pool, db, bot, cache):
    return TransferData(
        pool=pool,
        db=db,
        cache=cache
    )

@pytest.fixture(scope='session')
def state(bot, storage):
    state = FSMContext(
        bot=bot, storage=storage,
        key=StorageKey(user_id=TEST_USER.id, bot_id=bot.id, chat_id=TEST_CHAT.id)
    )

    return state