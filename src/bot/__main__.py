""" This file represent startup bot logic"""
import asyncio
import logging

from aiogram import Bot

from src.bot.dispatcher import get_dispatcher, get_redis_storage
from src.bot.keyboards import set_main_menu
from src.bot.structures import TransferData
from src.cache import Cache
from src.configuration import conf
from src.db import create_session_maker


async def start_bot():
    """This function will start bot with polling mode"""
    bot = Bot(token=conf.bot.token, parse_mode='HTML')
    cache = Cache()
    storage = get_redis_storage(redis=cache)
    dp = get_dispatcher(storage=storage, bot=bot)

    await set_main_menu(bot)

    await bot.delete_webhook(drop_pending_updates=True)
    # TODO: приделать webhook
    await dp.start_polling(
        bot,
        allowed_updates=dp.resolve_used_update_types(),
        **TransferData(pool=await create_session_maker(), cache=cache)
    )


if __name__ == "__main__":
    logging.basicConfig(level=conf.logging_level,
                        format="%(asctime)s - [%(levelname)s] -  %(name)s - "
                               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
                        )
    logger = logging.getLogger(__name__)
    try:
        asyncio.run(start_bot())
        logger.info('Bot started')
    except (KeyboardInterrupt, SystemExit):
        logger.info('Bot stopped')
