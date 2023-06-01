from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.bot.lexicon import DEVELOPER_LINK
from src.bot.settings.settings import tg_bot_admin


def dev_link_kb() -> InlineKeyboardMarkup:
    developer_link: InlineKeyboardButton = InlineKeyboardButton(
        text=DEVELOPER_LINK,
        url=f'tg://user?id={tg_bot_admin[0]}')

    donate_link = ...  # TODO: реализовать донат систему

    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
        inline_keyboard=[[developer_link]])

    return keyboard
