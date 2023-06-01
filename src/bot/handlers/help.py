""" This file represents a help logic """

from aiogram import Router, types
from aiogram.filters import Command

from src.bot.keyboards import dev_link_kb
from src.bot.lexicon import render_template

help_router = Router(name="help")


@help_router.message(Command(commands="help"))
async def help(message: types.Message):
    """Help command handler"""
    return await message.answer(text=render_template('help.html'), reply_markup=dev_link_kb())
