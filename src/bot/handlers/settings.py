""" This file represents a settings logic """

from aiogram import Router, types, F
from aiogram.filters import Command, or_f, and_f
from aiogram.fsm.context import FSMContext

from src.bot.keyboards import make_many_rows_keyboard
from src.bot.lexicon import settings_text
from src.bot.structures import SettingsStates
from src.db.models import TestStatus

settings_router = Router(name="settings")


async def set_changer(message: types.Message, db, state: FSMContext):
    """
    Make changes of settings in db
    """
    data = await state.get_data()

    test: TestStatus = await db.test.get(message.from_user.id)

    await db.test.update(
        user_id=message.from_user.id,
        status=False,
        theme=settings_text.AVAILABLE_THEME_NAMES[data['chosen_theme']],
        number_of_questions=data['chosen_amount'],
        show_correct_anwser_alert=data['show_correct_answer_alert'],
        question=0,
        score=0
    )

    await db.session.commit()

# first step

@settings_router.message(Command(commands="settings"))
async def get_settings(message: types.Message, state: FSMContext):
    """
    Settings command handler
    Display theme selection menu
    """
    await state.set_state(SettingsStates.set_theme)

    return await message.answer(
        text=settings_text.SETTINGS_MAIN,
        reply_markup=make_many_rows_keyboard(settings_text.AVAILABLE_THEME_NAMES)
    )



@settings_router.message(
    SettingsStates.set_theme,
    F.text.in_(settings_text.AVAILABLE_THEME_NAMES)
)
async def theme_chosen(message: types.Message, state: FSMContext):
    """
    Successful theme selection
    Display number of questions selection menu
    """
    await state.update_data(chosen_theme=message.text)

    await state.set_state(SettingsStates.set_number_of_questions)

    return await message.answer(
        text=settings_text.CHOICE_NUM_OF_QUESTIONS,
        reply_markup=make_many_rows_keyboard(settings_text.AVAILABLE_QUESTION_AMOUNT)
    )



@settings_router.message(SettingsStates.set_theme)
async def theme_chosen_incorrectly(message: types.Message):
    """
    Incorrect theme selected
    Display theme selection menu again
    """
    return await message.answer(
        text=settings_text.INCORRECT_THEME_NAME,
        reply_markup=make_many_rows_keyboard(settings_text.AVAILABLE_THEME_NAMES)
    )

# second step

@settings_router.message(
    SettingsStates.set_number_of_questions,
    or_f(
        and_f(F.text.isdigit(),   
            lambda message: int(message.text) >= 5),
        F.text == settings_text.AVAILABLE_QUESTION_AMOUNT[1]
        )
)
async def questions_amount_chosen(message: types.Message, state: FSMContext):
    """
    Successful number of questions selection
    Display show correct answer alert selection menu
    """
    await state.update_data(
        chosen_amount=1000 if message.text==settings_text.AVAILABLE_QUESTION_AMOUNT[1] else int(message.text)
        )

    await state.set_state(SettingsStates.set_correct_answer_alert)
    
    return await message.answer(
        text=settings_text.CHOISE_CORRECT_ANSWER_ALERT,
        reply_markup=make_many_rows_keyboard(settings_text.AVAILABLE_OPTS_SHOW_CORRECT_ANSWER_ALERT)
    )
    



@settings_router.message(
    SettingsStates.set_number_of_questions,
    F.text == settings_text.AVAILABLE_QUESTION_AMOUNT[2]
)
async def questions_amount_chosen_different(message: types.Message, state: FSMContext):
    """
    Input number of questions 
    """
    return await message.answer(
        text=settings_text.ENTER_NUMBER_OF_QUESTIONS,
        reply_markup=types.ReplyKeyboardRemove()
    )


@settings_router.message(SettingsStates.set_number_of_questions)
async def questions_amount_chosen_incorrectly(message: types.Message):
    """
    Incorrect number of questions  selected
    Display theme number of questions  menu again
    """
    return await message.answer(
        text=settings_text.INCORRECT_NUM,
        reply_markup=make_many_rows_keyboard(settings_text.AVAILABLE_QUESTION_AMOUNT)
    )

# third step

@settings_router.message(
    SettingsStates.set_correct_answer_alert,
    F.text.in_(settings_text.AVAILABLE_OPTS_SHOW_CORRECT_ANSWER_ALERT)
)
async def alerts_chosen(message: types.Message, state: FSMContext, db):
    """
    Successful alerts selection
    Сompletion of settings
    """
    await state.update_data(show_correct_answer_alert=True if message.text == settings_text.AVAILABLE_OPTS_SHOW_CORRECT_ANSWER_ALERT[0] else False)

    await set_changer(message, db, state)

    await state.clear()

    return await message.answer(
        text=settings_text.SELECTED_PARAMS,
        reply_markup=types.ReplyKeyboardRemove()
    )


    
    
@settings_router.message(SettingsStates.set_correct_answer_alert)
async def alerts_chosen_incorrectly(message: types.Message):
    """
    Incorrect alerts selection
    Display show correct answer alert selection menu
    """
    return await message.answer(
        text=settings_text.INCORRECT_NUM,
        reply_markup=make_many_rows_keyboard(settings_text.AVAILABLE_OPTS_SHOW_CORRECT_ANSWER_ALERT)
    )  
    