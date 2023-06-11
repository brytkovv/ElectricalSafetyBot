import random

import pytest
from aiogram import Dispatcher
from aiogram.fsm.context import FSMContext

from src.bot.lexicon import settings_text
from src.bot.structures.fsm_groups import SettingsStates
from src.db.models import TestStatus
from tests.utils.handler_checker import command_is_handled
from tests.utils.mocked_bot import MockedBot
from tests.utils.updates import get_update, get_message, TEST_USER


@pytest.mark.asyncio
async def test_settings(bot: MockedBot, dp: Dispatcher, state: FSMContext, db):
    #  инициация
    await state.clear()
    await command_is_handled(bot, dp, state, db, '/settings', settings_text.SETTINGS_MAIN, SettingsStates.set_theme,
                             settings_text.AVAILABLE_THEME_NAMES)

    # первый шаг
    # проверяем неправильные значения
    [await command_is_handled(bot, dp, state, db, i, settings_text.INCORRECT_THEME_NAME, SettingsStates.set_theme,
                              settings_text.AVAILABLE_THEME_NAMES) for i in settings_text.INCORRECT_THEME_NAMES]

    # проверяем правильные  
    for i in settings_text.AVAILABLE_THEME_NAMES:
        await command_is_handled(bot, dp, state, db, i, settings_text.CHOICE_NUM_OF_QUESTIONS,
                                 SettingsStates.set_number_of_questions,
                                 settings_text.AVAILABLE_QUESTION_AMOUNT)
        await state.set_state(SettingsStates.set_theme)

        await command_is_handled(bot, dp, state, db, 'Назад', settings_text.INCORRECT_THEME_NAME,
                                 SettingsStates.set_theme,
                                 settings_text.AVAILABLE_THEME_NAMES)

    await command_is_handled(
        bot, dp, state, db,
        random.choice(list(settings_text.AVAILABLE_THEME_NAMES.keys())),
        settings_text.CHOICE_NUM_OF_QUESTIONS,
        SettingsStates.set_number_of_questions,
        settings_text.AVAILABLE_QUESTION_AMOUNT
    )

    # второй шаг
    [await command_is_handled(bot, dp, state, db, i, settings_text.INCORRECT_NUM,
                              SettingsStates.set_number_of_questions,
                              settings_text.AVAILABLE_QUESTION_AMOUNT) for i in settings_text.INCORRECT_QUESTION_AMOUNT]

    for i in settings_text.CORRECT_QUESTION_AMOUNT:
        await command_is_handled(bot, dp, state, db, i, settings_text.CHOISE_CORRECT_ANSWER_ALERT,
                                 SettingsStates.set_correct_answer_alert,
                                 settings_text.AVAILABLE_OPTS_SHOW_CORRECT_ANSWER_ALERT)
        await state.set_state(SettingsStates.set_number_of_questions)

        command = get_update(get_message('Назад'))
        await dp.feed_update(bot, command)

    await command_is_handled(
        bot, dp, state, db,
        'Свое количество',
        settings_text.ENTER_NUMBER_OF_QUESTIONS,
        SettingsStates.set_number_of_questions,
        None
    )

    await command_is_handled(
        bot, dp, state, db,
        '55',
        settings_text.CHOISE_CORRECT_ANSWER_ALERT,
        SettingsStates.set_correct_answer_alert,
        settings_text.AVAILABLE_OPTS_SHOW_CORRECT_ANSWER_ALERT
    )

    # третий шаг
    [await command_is_handled(bot, dp, state, db, i, settings_text.INCORRECT_NUM,
                              SettingsStates.set_correct_answer_alert,
                              settings_text.AVAILABLE_OPTS_SHOW_CORRECT_ANSWER_ALERT) for i in
     settings_text.INCORRECT_OPTS_SHOW_CORRECT_ANSWER_ALERT]

    for i in settings_text.AVAILABLE_OPTS_SHOW_CORRECT_ANSWER_ALERT:
        await state.clear()
        await command_is_handled(bot, dp, state, db, '/settings', settings_text.SETTINGS_MAIN, SettingsStates.set_theme,
                                 settings_text.AVAILABLE_THEME_NAMES)

        await command_is_handled(
            bot, dp, state, db,
            random.choice(list(settings_text.AVAILABLE_THEME_NAMES.keys())),
            settings_text.CHOICE_NUM_OF_QUESTIONS,
            SettingsStates.set_number_of_questions,
            settings_text.AVAILABLE_QUESTION_AMOUNT
        )

        await command_is_handled(
            bot, dp, state, db,
            random.choice(list(range(5, 1000))),
            settings_text.CHOISE_CORRECT_ANSWER_ALERT,
            SettingsStates.set_correct_answer_alert,
            settings_text.AVAILABLE_OPTS_SHOW_CORRECT_ANSWER_ALERT
        )

        await command_is_handled(bot, dp, state, db, i, settings_text.SELECTED_PARAMS, None, None)
        await state.set_state(SettingsStates.set_correct_answer_alert)

        test: TestStatus = await db.test.get(TEST_USER.id)

        assert test.theme in settings_text.AVAILABLE_THEME_NAMES.values()
        assert test.number_of_questions >= 5, type(test.number_of_questions) == int
        assert type(test.show_correct_anwser_alert) == bool
