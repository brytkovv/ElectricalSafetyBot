import pytest
from aiogram import Dispatcher
from aiogram.methods import SendMessage

from src.bot.keyboards import dev_link_kb
from src.bot.lexicon import render_template
from tests.utils.mocked_bot import MockedBot
from tests.utils.updates import get_update, get_message


@pytest.mark.asyncio
async def test_handler_help(bot: MockedBot, dp: Dispatcher):
    help_command = get_update(get_message('/help'))
    result = await dp.feed_update(bot, help_command)
    assert isinstance(result, SendMessage)
    assert result.text == render_template('help.html')
    assert result.reply_markup == dev_link_kb()
