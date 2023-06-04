import pytest
from aiogram import Dispatcher
from aiogram.methods import SendMessage

from src.bot.lexicon import render_template
from tests.utils.mocked_bot import MockedBot
from tests.utils.updates import get_update, get_message, TEST_USER

users_data = [
    {
        "user_id": 123,
        "user_name": "Слава"
    },
    {
        "user_id": 12,
        "user_name": "Differ"
    }
]

attempts_data = [
    {
        "attempt_id": "0738c864-9ebd-4ec4-a70a-b7203373223b",
        "user_id": 12,
        "result": 0.2
    },
    {
        "attempt_id": "1fff68de-8942-4ea6-b3cf-d2ce4d6b5934",
        "user_id": 123,
        "result": 0.6
    },
    {
        "attempt_id": "5010d717-475f-413f-aa66-f0d325d3e5ef",
        "user_id": 123,
        "result": 0.8
    },
    {
        "attempt_id": "52c38208-13db-45e4-9346-a2acb06c68bb",
        "user_id": 12,
        "result": 0.9
    },
    {
        "attempt_id": "690ec65c-fc14-4517-8f5d-7df2cc54a4a4",
        "user_id": 123,
        "result": 0.8
    }
]


async def dp_filler(db):
    for i in users_data:
        await db.user.new(user_id=i["user_id"], user_name=i["user_name"])

    for i in attempts_data:
        await db.attempt.new(attempt_id=i["attempt_id"], user_id=i["user_id"], result=i["result"])


@pytest.mark.asyncio
async def test_record(bot: MockedBot, dp: Dispatcher, db):
    await dp_filler(db)

    record_command = get_update(get_message('/record')) # TODO: вызываются разные объеты дб
    result = await dp.feed_update(bot, record_command)
    assert isinstance(result, SendMessage)

    attempts, successful = await db.attempt.get_stat(user_id=TEST_USER.id)

    assert result.text == render_template('record.html', attempts=attempts, successful=successful)
