""" This file represents a alerts logic """

from aiogram import Router

from src.bot.settings.settings import tg_bot_admin

alerts_router = Router(name="alert")


async def start_the_bot(bot):
    await bot.send_message(tg_bot_admin[0], text='Бот запущен!')


async def stop_the_bot(bot):
    await bot.send_message(tg_bot_admin[0], text='Бот остановлен!')


alerts_router.startup.register(start_the_bot)
alerts_router.shutdown.register(stop_the_bot)
