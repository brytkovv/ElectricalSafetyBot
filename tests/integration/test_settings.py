import random
import pytest
from aiogram import Dispatcher
from aiogram.methods import SendMessage
from aiogram.fsm.context import FSMContext

from src.bot.keyboards import make_many_rows_keyboard
from src.bot.lexicon import settings_text
from src.bot.structures.fsm_groups import SettingsStates
from tests.utils.mocked_bot import MockedBot
from tests.utils.updates import get_update, get_message


@pytest.mark.asyncio
async def test_settings(bot: MockedBot, dp: Dispatcher, state: FSMContext):
    
    INCORRECT_THEME_NAMES = [' ', 5, '5', 'Четвертая', 'Оповещать']
    
    INCORRECT_QUESTION_AMOUNT = [1, 2, 3, 4, 2.4, 212.2, 'V группа допуска', 'Оповещать', '3']
    
    INCORRECT_OPTS_SHOW_CORRECT_ANSWER_ALERT = ['Не оповещать', 100, 'V группа допуска', '']
           
    async def command_is_hadled(text, expected, expected_state, kb=None):
        commanda = get_update(get_message(text))
        result = await dp.feed_update(bot, commanda)
        
        assert isinstance(result, SendMessage), f'{text}'
        assert result.text == expected
        assert result.reply_markup == make_many_rows_keyboard(kb)
        assert state.get_state() == expected_state
        
    #  инициация
    await state.clear()

    set_com = get_update(get_message('/settings'))
    result = await dp.feed_update(bot, set_com)

    assert isinstance(result, SendMessage), f'{result}111'

    await command_is_hadled('/settings', settings_text.SETTINGS_MAIN, SettingsStates.set_theme, settings_text.AVAILABLE_THEME_NAMES)

    # первый шаг
    # проверяем неправильные значения
    [await command_is_hadled(i, settings_text.INCORRECT_THEME_NAME, SettingsStates.set_theme, settings_text.AVAILABLE_THEME_NAMES) for i in INCORRECT_THEME_NAMES]
    
    # проверяем правильные  
    for i in settings_text.AVAILABLE_THEME_NAMES:
        await command_is_hadled(i, settings_text.CHOICE_NUM_OF_QUESTIONS, SettingsStates.set_number_of_questions, settings_text.AVAILABLE_QUESTION_AMOUNT)
        await state.set_state(SettingsStates.set_theme)
        
        # command = get_update(get_message('Назад')) # произвольное неподходящее слово для обновления состояния
        # await dp.feed_update(bot, command)
        
        await command_is_hadled('Назад', settings_text.INCORRECT_THEME_NAME, SettingsStates.set_theme, settings_text.AVAILABLE_THEME_NAMES)
        
        
    await command_is_hadled(
        random.choice(settings_text.AVAILABLE_THEME_NAMES), 
        settings_text.CHOICE_NUM_OF_QUESTIONS, 
        SettingsStates.set_number_of_questions, 
        settings_text.AVAILABLE_QUESTION_AMOUNT
        )
    
    # второй шаг
    [await command_is_hadled(i, settings_text.INCORRECT_NUM, SettingsStates.set_number_of_questions, settings_text.AVAILABLE_QUESTION_AMOUNT) for i in INCORRECT_QUESTION_AMOUNT]
    
    for i in ['5', '10', '20', '50', '100', 'Все', 7, 99, 400]:
        await command_is_hadled(i, settings_text.CHOISE_CORRECT_ANSWER_ALERT, SettingsStates.set_correct_answer_alert, settings_text.AVAILABLE_OPTS_SHOW_CORRECT_ANSWER_ALERT)
        await state.set_state(SettingsStates.set_number_of_questions)
        
        command = get_update(get_message('Назад')) 
        await dp.feed_update(bot, command)
        
    await command_is_hadled(
        'Свое количество', 
        settings_text.ENTER_NUMBER_OF_QUESTIONS, 
        SettingsStates.set_correct_answer_alert, 
        None
        )
    
    await command_is_hadled(
        '55', 
        settings_text.CHOISE_CORRECT_ANSWER_ALERT, 
        SettingsStates.set_correct_answer_alert, 
        settings_text.AVAILABLE_OPTS_SHOW_CORRECT_ANSWER_ALERT
        )

    # третий шаг
    [await command_is_hadled(i, settings_text.INCORRECT_NUM, SettingsStates.set_number_of_questions, settings_text.AVAILABLE_QUESTION_AMOUNT) for i in INCORRECT_QUESTION_AMOUNT]
    
    # проверяем что данные в дб поменялись
    
    
   