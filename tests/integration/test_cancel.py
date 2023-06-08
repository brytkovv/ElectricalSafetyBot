import pytest
from aiogram import Dispatcher
from aiogram.methods import SendMessage
from aiogram.dispatcher.event.bases import UNHANDLED
from aiogram.fsm.context import FSMContext

from src.bot.lexicon import settings_text
from src.bot.structures.fsm_groups import SettingsStates
from tests.utils.mocked_bot import MockedBot
from tests.utils.updates import get_update, get_message


@pytest.mark.asyncio
async def test_cancel(bot: MockedBot, dp: Dispatcher, state: FSMContext):
    cancel_vars = [
        '/cancel',
        settings_text.BUTTON_CANCEL,
        'Отмена',
        'отмена',
        'оТмена'
        ]
    
    async def command_is_unhadled(text):    # TODO: вынести в утилс
        command = get_update(get_message(text))
        result = await dp.feed_update(bot, command)
        assert isinstance(result, type(UNHANDLED))

    async def command_is_hadled(text, expected):
        command = get_update(get_message(text))
        result = await dp.feed_update(bot, command)
        
        assert isinstance(result, SendMessage), text
        assert result.text == expected
        assert await state.get_data() == {}


    await state.clear()
    [await command_is_unhadled(text) for text in cancel_vars]
    
    await state.set_state(SettingsStates.set_theme)
    [await command_is_hadled(text, settings_text.DISCARD_CHANGES) for text in cancel_vars]
    
    await state.set_state(SettingsStates.set_number_of_questions)
    [await command_is_hadled(text, settings_text.DISCARD_CHANGES) for text in cancel_vars]
    
    await state.set_state(SettingsStates.set_correct_answer_alert) 
    [await command_is_hadled(text, settings_text.DISCARD_CHANGES) for text in cancel_vars]
    