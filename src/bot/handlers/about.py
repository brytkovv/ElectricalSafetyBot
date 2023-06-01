""" This file represents about page logic """

from aiogram import Router, types
from aiogram.filters import Command

from src.bot.keyboards import dev_link_kb
from src.bot.lexicon import render_template

about_router = Router(name="about")


@about_router.message(Command(commands="about"))
async def about(message: types.Message):
    """About command handler"""

    return await message.answer(text=render_template('about.html'), reply_markup=dev_link_kb())
