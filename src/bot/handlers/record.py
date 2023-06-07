""" This file represents a record logic """

from aiogram import Router, types
from aiogram.filters import Command

from src.bot.lexicon import render_template

record_router = Router(name="record")


@record_router.message(Command(commands="record"))
async def record(message: types.Message, db):
    """record command handler"""
    attempts, successful = await db.attempt.get_stat(user_id=message.from_user.id)

    await message.answer(render_template('record.html', attempts=attempts, successful=successful))

    return message.from_user.id, attempts, successful # TODO: подумать, удобно ли это