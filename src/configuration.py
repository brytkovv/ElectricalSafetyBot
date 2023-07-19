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

    name: str = getenv("POSTGRES_DB")
    user: str = getenv("POSTGRES_USER", "docker")
    passwd: str = getenv("POSTGRES_PASSWORD", None)
    port: int = int(getenv("POSTGRES_PORT", 5432))
    host: str = getenv("POSTGRES_HOST", "db")

    driver: str = "asyncpg"
    database_system: str = "postgresql"

    def build_connection_str(self) -> str:
        """
        This function build a connection string
        """
        return URL.create(
            drivername=f"{self.database_system}+{self.driver}",
            username=self.user,
            database=self.name,
            password=self.passwd,
            port=self.port,
            host=self.host,
        ).render_as_string(hide_password=False)


@dataclass
class RedisConfig:
    """Redis connection variables"""

    db: str = int(getenv("REDIS_DATABASE", 1))
    host: str = getenv("REDIS_HOST", "redis")
    port: int = int(getenv("REDIS_PORT", 6379))
    passwd: str | int = getenv("REDIS_PASSWORD", None)
    username: int = getenv("REDIS_USERNAME", None)
    state_ttl: int = getenv("REDIS_TTL_STATE", None)
    data_ttl: int = getenv("REDIS_TTL_DATA", None)

    def build_connection_str(self) -> str:
        redis = Redis(
            host=self.host,
            db=self.db,
            port=self.port,
            password=self.passwd
            # username=self.username
        )
        return redis


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
