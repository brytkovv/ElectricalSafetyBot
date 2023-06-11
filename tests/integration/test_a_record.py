import pytest
from aiogram import Dispatcher
from aiogram.methods import SendMessage

from src.bot.lexicon import render_template
from tests.utils.mocked_bot import MockedBot
from tests.utils.updates import get_update, get_message, TEST_USER


@pytest.mark.asyncio
async def test_record(bot: MockedBot, dp: Dispatcher, db):
    record_command = get_update(get_message('/record'))
    result = await dp.feed_update(bot, record_command, db=db)
    assert isinstance(result, SendMessage)

    attempts, successful = await db.attempt.get_stat(user_id=TEST_USER.id)

    assert result.text == render_template('record.html', attempts=attempts, successful=successful)
    assert attempts == 4
    assert successful == 3
