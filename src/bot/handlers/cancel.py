""" This file represents a cancel logic """

from aiogram import Router, types, F
from aiogram.filters import Command, Text, or_f, and_f
from aiogram.fsm.context import FSMContext

from src.bot.lexicon import settings_text
from src.bot.structures import SettingsStates

cancel_router = Router(name="cancel")


@cancel_router.message(
        and_f(
            or_f(
                SettingsStates.set_number_of_questions, 
                SettingsStates.set_theme, 
                SettingsStates.set_correct_answer_alert
            ),
            or_f(
                F.text == settings_text.BUTTON_CANCEL,
                Command(commands=["cancel"]), 
                Text(text="отмена", ignore_case=True)
            )
        )
)
async def cancel(message: types.Message, state: FSMContext):
    await state.clear()

    return await message.answer(
        text=settings_text.DISCARD_CHANGES,
        reply_markup=types.ReplyKeyboardRemove()
    )


