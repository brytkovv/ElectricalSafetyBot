""" This file represents a cancel logic """

from aiogram import Router, types, F
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext

from src.bot.lexicon import settings_text
from src.bot.structures import SettingsStates

cancel_router = Router(name="cancel")


@cancel_router.message(Command(commands=["cancel"]))
@cancel_router.message(Text(text="отмена", ignore_case=True))
@cancel_router.message(
    SettingsStates.set_number_of_questions,
    F.text == settings_text.BUTTON_CANCEL
)
@cancel_router.message(
    SettingsStates.set_theme,
    F.text == settings_text.BUTTON_CANCEL
)
async def cancel(message: types.Message, state: FSMContext):
    await message.answer(
        text=settings_text.DISCARD_CHANGES,
        reply_markup=types.ReplyKeyboardRemove()
    )

    await state.clear()
