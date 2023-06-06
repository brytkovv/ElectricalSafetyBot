from aiogram.fsm.state import StatesGroup, State


class SettingsStates(StatesGroup):
    set_theme = State()
    set_number_of_questions = State()
    set_correct_answer_alert = State()
