""" This file represents a top logic """

from aiogram import Router, types
from aiogram.filters import Command

from src.bot.lexicon import render_template

top_router = Router(name="top")


@top_router.message(Command(commands="top"))
async def top(message: types.Message, db):
    """top command handler"""
    attempts = await db.attempt.get_top()

    text = render_template(
        'top.html',
        top=[f'{i[0]}: {i[1]}' for i in attempts],
    )

    return await message.answer(text)
