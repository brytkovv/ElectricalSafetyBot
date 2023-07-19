""" This file represents a admin command logic """

from aiogram import Router, types
from aiogram.filters import Command

from src.bot.utils.dumpdata import dump, restore
from src.configuration import conf

admin_router = Router(name="alert")


async def start_the_bot(bot):
    [await bot.send_message(tg_id, text='Бот запущен!') for tg_id in conf.admin_ids]


async def stop_the_bot(bot):
    [await bot.send_message(tg_id, text='Бот остановлен!') for tg_id in conf.admin_ids]


admin_router.startup.register(start_the_bot)
admin_router.shutdown.register(stop_the_bot)


@admin_router.message(lambda message: message.from_user.id in conf.admin_ids, Command(commands="statistic"))
async def stat(message: types.Message, db):
    """Statisic for admin command handler"""
    attempts = await db.attempt.get_num_of_attempts()
    users = await db.user.get_num_of_users()

    # TODO: добавить статистику за день, может изображением, сделать template

    return await message.answer(
        f'<b>Пользователей:</b> {users[0] if users else 0}\n<b>Попыток всего:</b>  {attempts[0] if attempts else 0}'
    )


@admin_router.message(lambda message: message.from_user.id in conf.admin_ids, Command(commands="dump_to_csv"))
async def dump_to_csv(message: types.Message, db):

    await db.user.data_to_csv()
    await db.attempt.data_to_csv()
    await db.test.data_to_csv()

    return await message.answer('Дамп создан')

@admin_router.message(lambda message: message.from_user.id in conf.admin_ids, Command(commands="dump"))
async def _dump(message: types.Message, db): # сделать по расписанию?
    await dump()

    return await message.answer('Дамп создан') # TODO: при успешном


@admin_router.message(lambda message: message.from_user.id in conf.admin_ids, Command(commands="restore"))
async def _restore(message: types.Message, db):

    await db.attempt.delete_data()
    await db.test.delete_data()
    await db.user.delete_data()

    await db.session.commit()

    await restore() # TODO: сделать выбор даты, сделать подпункт подтверждения

    return await message.answer('База данных восстановлена') # TODO: при успешном
