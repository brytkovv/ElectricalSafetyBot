""" This file represents a record logic """

from aiogram import Router, types
from aiogram.filters import Command

from src.bot.lexicon import render_template

record_router = Router(name="record")


@record_router.message(Command(commands="record"))
async def record(message: types.Message, db):
    """record command handler"""
    stat = await db.attempt.get_stat(user_id=message.from_user.id)
    successful = sum([0 if i.result < 0.8 else 1 for i in stat])

    return await message.answer(render_template('record.html', attempts=len(stat), successful=successful))
