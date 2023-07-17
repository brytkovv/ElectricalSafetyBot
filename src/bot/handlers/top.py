""" This file represents a top logic """

from aiogram import Router, types
from aiogram.filters import Command

from src.bot.lexicon import render_template

top_router = Router(name="top")


@top_router.message(Command(commands="top"))
async def top(message: types.Message, db):
    """top command handler"""
    stat = await db.attempt.get_top(user_id=message.from_user.id)
    text = render_template('top.html', top=stat)

    return await message.answer(text)
