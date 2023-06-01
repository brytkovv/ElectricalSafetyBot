from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from src.bot.lexicon import settings_text


def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    """
    Создаёт реплай-клавиатуру с кнопками в один ряд
    :param items: список текстов для кнопок
    :return: объект реплай-клавиатуры
    """
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)


def make_many_rows_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    """
    Создаёт реплай-клавиатуру с кнопками в строку
    :param items: список текстов для кнопок
    :return: объект реплай-клавиатуры
    """
    row = [[KeyboardButton(text=i) for i in item] if isinstance(item, list) else [KeyboardButton(text=item)] for item in
           items]
    row.append([KeyboardButton(text=settings_text.BUTTON_CANCEL)])  # TODO: всегда отмена?!

    return ReplyKeyboardMarkup(keyboard=row, resize_keyboard=True)
