import pytest
from aiogram import Dispatcher

from tests.utils.mocked_bot import MockedBot
from tests.utils.updates import get_update, get_message, TEST_USER
from tests.utils.fake_data_for_db import users_data, attempts_data


async def dp_filler(db):
    for i in users_data:
        await db.user.new(user_id=i["user_id"], user_name=i["user_name"])

    for i in attempts_data:
        await db.attempt.new(attempt_id=i["attempt_id"], user_id=i["user_id"], result=i["result"])


@pytest.mark.asyncio
async def test_record(bot: MockedBot, dp: Dispatcher, db):
    
    await dp_filler(db)

    record_command = get_update(get_message('/record')) 
    user_id, attempts, successful = await dp.feed_update(bot, record_command)
    
    assert user_id == TEST_USER.id
    assert attempts == 3
    assert successful == 2 # TODO: вручную посчитанные значения.
