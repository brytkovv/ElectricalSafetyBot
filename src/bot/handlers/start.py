""" This file represents a start logic """

from aiogram import Router, types
from aiogram.filters import CommandStart

from src.bot.keyboards import dev_link_kb
from src.bot.lexicon import render_template

start_router = Router(name="start")


@start_router.message(CommandStart())
async def start(message: types.Message):
    """Start command handler"""
    return await message.answer(text=render_template('start.html'), reply_markup=dev_link_kb())
