import pytest
from aiogram import Dispatcher
from aiogram.methods import SendMessage

from src.bot.keyboards import dev_link_kb
from src.bot.lexicon import render_template
from tests.utils.mocked_bot import MockedBot
from tests.utils.updates import get_update, get_message


@pytest.mark.asyncio
async def test_start(bot: MockedBot, dp: Dispatcher):
    start_command = get_update(get_message('/start'))
    result = await dp.feed_update(bot, start_command)
    assert isinstance(result, SendMessage)
    assert result.text == render_template('start.html')
    assert result.reply_markup == dev_link_kb()
