""" This file represents configurations from files and environment"""
import logging
import os
from dataclasses import dataclass
from os import getenv

import dotenv
from redis.asyncio.client import Redis
from sqlalchemy.engine import URL

dotenv.load_dotenv()

pwd = os.getcwd()


@dataclass
class DatabaseConfig:
    """Database connection variables"""

    db_url: str = getenv("DATABASE_URL")

    def build_connection_str(self) -> str:
        """
        Возвращает строку подключения, корректируя схему, если это необходимо.
        """
        if self.db_url.startswith("postgres://"):
            return self.db_url.replace("postgres://", "postgresql+asyncpg://", 1)
        return self.db_url


@dataclass
class RedisConfig:
    """Redis connection variables"""

    redis_url: str = getenv("REDIS_URL")
    state_ttl: int = getenv("REDIS_TTL_STATE", None)
    data_ttl: int = getenv("REDIS_TTL_DATA", None)

    def build_connection_str(self) -> str:
        return self.redis_url


@dataclass
class BotConfig:
    """Bot configuration"""

    token: str = getenv("BOT_TOKEN")


@dataclass
class Configuration:
    """All in one configuration's class"""

    debug = bool(getenv("DEBUG"))
    logging_level = int(getenv("LOGGING_LEVEL", logging.INFO))

    db = DatabaseConfig()
    redis = RedisConfig()
    bot = BotConfig()

    admin_ids = list(int(i) for i in getenv("TG_BOT_ADMIN").split(', '))


conf = Configuration()
