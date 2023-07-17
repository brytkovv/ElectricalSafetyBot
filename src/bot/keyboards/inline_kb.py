from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.bot.lexicon import DEVELOPER_LINK
from src.configuration import conf


def dev_link_kb() -> InlineKeyboardMarkup:
    developer_link: InlineKeyboardButton = InlineKeyboardButton(
        text=DEVELOPER_LINK,
        url=f'tg://user?id={conf.admin_ids[0]}')

    donate_link = ...  # TODO: реализовать донат систему

    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
        inline_keyboard=[[developer_link]])

    return keyboard
