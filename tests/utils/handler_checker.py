from aiogram import Dispatcher
from aiogram.dispatcher.event.bases import UNHANDLED
from aiogram.fsm.context import FSMContext
from aiogram.methods import SendMessage

from src.bot.keyboards import make_many_rows_keyboard
from tests.utils.mocked_bot import MockedBot
from tests.utils.updates import get_update, get_message


async def command_is_handled(
        bot: MockedBot,
        dp: Dispatcher,
        state: FSMContext,
        db,
        text,
        expected,
        expected_state=None,
        kb=None
):
    commanda = get_update(get_message(text))  # TODO: разбрить на две функции?
    result = await dp.feed_update(bot, commanda, db=db)

    assert isinstance(result, SendMessage), f'{text} {result}'
    assert result.text == expected
    if kb:
        assert result.reply_markup == make_many_rows_keyboard(kb)
    assert await state.get_state() == expected_state


async def command_is_unhadled(
        bot: MockedBot,
        dp: Dispatcher,
        db,
        text
):
    command = get_update(get_message(text))
    result = await dp.feed_update(bot, command, db=db)

    assert isinstance(result, type(UNHANDLED))
