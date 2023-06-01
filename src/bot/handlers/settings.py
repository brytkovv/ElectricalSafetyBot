""" This file represents a settings logic """

from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from src.bot.keyboards import make_many_rows_keyboard
from src.bot.lexicon import settings_text
from src.bot.structures import SettingsStates
from src.db.models import TestStatus

settings_router = Router(name="settings")


async def set_changer(message: types.Message, db, state: FSMContext):
    data = await state.get_data()

    test: TestStatus = await db.test.get(message.from_user.id)

    await db.test.update(
        user_id=message.from_user.id,
        status=False,
        theme=settings_text.AVAILABLE_THEME_NAMES[data['chosen_theme']],
        number_of_questions=data['chosen_amount'],
        question=0,
        score=0
    )

    await db.session.commit()


@settings_router.message(Command(commands="settings"))
async def get_settings(message: types.Message, state: FSMContext):
    """Settings command handler"""
    await message.answer(
        text=settings_text.SETTINGS_MAIN,
        reply_markup=make_many_rows_keyboard(settings_text.AVAILABLE_THEME_NAMES)
    )
    await state.set_state(SettingsStates.set_theme)


@settings_router.message(
    SettingsStates.set_theme,
    F.text.in_(settings_text.AVAILABLE_THEME_NAMES)
)
async def theme_chosen(message: types.Message, state: FSMContext):
    await state.update_data(chosen_theme=message.text)

    await message.answer(
        text=settings_text.CHOICE_NUM_OF_QUESTIONS,
        reply_markup=make_many_rows_keyboard(settings_text.AVAILABLE_QUESTION_AMOUNT)
    )
    await state.set_state(SettingsStates.set_number_of_questions)


@settings_router.message(SettingsStates.set_theme)
async def theme_chosen_incorrectly(message: types.Message):
    await message.answer(
        text=settings_text.INCORRECT_THEME_NAME,
        reply_markup=make_many_rows_keyboard(settings_text.AVAILABLE_THEME_NAMES)
    )


@settings_router.message(
    SettingsStates.set_number_of_questions,
    F.text.isdigit(),
    lambda message: int(message.text) >= 5
)
async def questions_amount_chosen_num(message: types.Message, state: FSMContext, db):
    await state.update_data(chosen_amount=int(message.text))
    await message.answer(
        text=settings_text.SELECTED_PARAMS,
        reply_markup=types.ReplyKeyboardRemove()
    )

    await set_changer(message, db, state)

    await state.clear()


@settings_router.message(
    SettingsStates.set_number_of_questions,
    F.text == settings_text.AVAILABLE_QUESTION_AMOUNT[1]
)
async def questions_amount_chosen_all(message: types.Message, state: FSMContext, db):
    await state.update_data(
        chosen_amount=1000)
    await message.answer(
        text=settings_text.SELECTED_ALL_QUESTS,
        reply_markup=types.ReplyKeyboardRemove()
    )

    await set_changer(message, db, state)

    await state.clear()


@settings_router.message(
    SettingsStates.set_number_of_questions,
    F.text == settings_text.AVAILABLE_QUESTION_AMOUNT[2]
)
async def questions_amount_chosen_different(message: types.Message, state: FSMContext):
    await state.update_data(chosen_amount=message.text)
    await message.answer(
        text=settings_text.ENTER_NUMBER_OF_QUESTIONS,
        reply_markup=types.ReplyKeyboardRemove()
    )


@settings_router.message(SettingsStates.set_number_of_questions)
async def questions_amount_chosen_incorrectly(message: types.Message):
    await message.answer(
        text=settings_text.INCORRECT_NUM,
        reply_markup=make_many_rows_keyboard(settings_text.AVAILABLE_QUESTION_AMOUNT)
    )
