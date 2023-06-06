""" This file represents a cancel logic """

from aiogram import Router, types, F
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext

from src.bot.lexicon import settings_text
from src.bot.structures import SettingsStates

cancel_router = Router(name="cancel")


@cancel_router.message(
        *[state for state in [SettingsStates.set_number_of_questions, SettingsStates.set_theme, SettingsStates.set_correct_answer_alert] if state],
        *[i for i in [F.text == settings_text.BUTTON_CANCEL, Command(commands=["cancel"]), Text(text="отмена", ignore_case=True)] if i]
)
async def cancel(message: types.Message, state: FSMContext):
    await message.answer(
        text=settings_text.DISCARD_CHANGES,
        reply_markup=types.ReplyKeyboardRemove()
    )

    await state.clear()


