import pytest
from aiogram import Dispatcher
from aiogram.fsm.context import FSMContext

from src.bot.lexicon import settings_text
from src.bot.structures.fsm_groups import SettingsStates
from tests.utils.handler_checker import command_is_handled, command_is_unhadled
from tests.utils.mocked_bot import MockedBot


@pytest.mark.asyncio
async def test_cancel(bot: MockedBot, dp: Dispatcher, db, state: FSMContext):
    cancel_vars = [
        '/cancel',
        settings_text.BUTTON_CANCEL,
        'Отмена',
        'отмена',
        'оТмена'
    ]

    await state.clear()
    [await command_is_unhadled(bot, dp, db, text) for text in cancel_vars]

    for text in cancel_vars:
        await state.set_state(SettingsStates.set_theme)
        await command_is_handled(bot, dp, state, db, text, settings_text.DISCARD_CHANGES)

        await state.set_state(SettingsStates.set_number_of_questions)
        await command_is_handled(bot, dp, state, db, text, settings_text.DISCARD_CHANGES)

        await state.set_state(SettingsStates.set_correct_answer_alert)
        await command_is_handled(bot, dp, state, db, text, settings_text.DISCARD_CHANGES)
