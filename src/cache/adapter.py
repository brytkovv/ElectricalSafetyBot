""" This file contains the cache adapter """
import asyncio
from datetime import timedelta
from typing import Any, List, Optional, final, overload

from redis.asyncio.client import Redis

from src.configuration import conf


def build_redis_client() -> Redis:
    """Build redis client"""
    client = Redis.from_url(conf.redis.redis_url)

    asyncio.create_task(client.ping())
    return client


class Cache:
    """Cache adapter"""

    def __init__(self, redis: Optional[Redis] = None):
        self.client = redis or build_redis_client()

    @property
    def redis_client(self) -> Redis:
        """
        Redis client which used in the cache adapter
        :return:
        """
        return self.client

    async def close(self):
        await self.client.close()

    @final
    async def get(self, key) -> Any:
        """
        Get a value from cache database
        :param key:
        :return: Value
        """
        return await self.client.get(str(key))

    @final
    async def set(self, key, value: Any, ex: None | int | timedelta = 0):
        """
        Set a value to cache database
        :param key: Key to set
        :param value: Value in a serializable type
        :param ex: Set the specified expire time, in seconds.
        :return: Nothing
        """
        if ex:
            await self.client.set(name=str(key), value=value, ex=ex)
        else:
            await self.client.set(name=str(key), value=value)

    async def expire(self, key, ttl: int | timedelta):
        await self.client.expire(name=key, time=ttl)

    @overload
    async def exists(self, key):
        """
        Check whether key has already defined or not
        :param key:
        :return: (bool) Result
        """
        ...

    @overload
    async def exists(self, *keys: List):
        """
        Overload of method to check many keys
        :param keys:
        :return:
        """
        ...

    async def exists(self, keys):
        if not isinstance(keys, list):
            return await self.client.exists(
                [
                    str(keys),
                ]
            )
        else:
            return await self.client.exists(*list(map(str, keys)))

    @final
    async def delete(self, key):
        await self.client.delete(str(key))
