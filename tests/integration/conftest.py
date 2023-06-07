from typing import Callable

import pytest
import pytest_asyncio
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

    # await database.teardown() # TODO: зачем нам тирдаун????
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
