from src.bot.handlers.about import about_router
from src.bot.handlers.admin_commands import admin_router
from src.bot.handlers.cancel import cancel_router
from src.bot.handlers.help import help_router
from src.bot.handlers.record import record_router
from src.bot.handlers.settings import settings_router
from src.bot.handlers.start import start_router
from src.bot.handlers.stop import stop_router
from src.bot.handlers.tester import tester_router
from src.bot.handlers.top import top_router

routers = (
    start_router,
    help_router,
    cancel_router,
    settings_router,
    top_router,
    record_router,
    stop_router,
    tester_router,
    admin_router,
    about_router
)
