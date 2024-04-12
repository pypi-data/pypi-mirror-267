import motor.motor_asyncio
from redis import asyncio as aioredis
from typing import Optional, Union
import msgpack

from .exceptions import NoConnectionError


class DBCommonConnector:
    def __init__(self, mongo_uri: str, db_name: str, redis_uri: str):
        """
        Constructor
        :param mongo_uri: MongoDB Connection URI
        :param system_db_name: DB Name
        :param verification_db_name: DB Name
        :param redis_uri: Redis Connection URI
        """
        self._mongo_uri = mongo_uri
        self._redis_uri = redis_uri
        self._db_name = db_name
        self._redis_client: Optional[aioredis.Redis] = None
        self._mongo_client: Optional[motor.motor_asyncio.AsyncIOMotorClient] = None
        self._db: Optional[motor.motor_asyncio.AsyncIOMotorDatabase] = None

    async def connect_db(self):
        """Create database connection."""
        self._mongo_client = motor.motor_asyncio.AsyncIOMotorClient(self._mongo_uri, tz_aware=True)
        self._db = self._mongo_client[self._db_name]
        self._redis_client = await aioredis.from_url(self._redis_uri)

    async def close_mongo_connection(self):
        """Close database connection."""
        if self._mongo_client:
            self._mongo_client.close()

    async def _cache_set_key(self, key: str, value: Union[dict, list], expire: Union[int, None] = 1800) -> bool:
        """
        Add Key:Value to Redis cache
        :param key: Key name
        :param value: Value Data dict
        :param expire: expiry time in seconds, default 1800s
        :return: if operation was successful
        """
        if self._redis_client is None:
            raise NoConnectionError("Redis client not connected")
        async with self._redis_client.client() as conn:
            if expire and expire > 0:
                ok = await conn.execute_command("SET", f"{key}", value, "EX", f"{expire}")
            else:
                ok = await conn.execute_command("SET", f"{key}", value)
            return bool(ok)

    async def _cache_get_key(self, key: str) -> Optional[Union[dict, list]]:
        """
        Retrieve value via key from Redis cache
        :param key: Key to retrieve data from
        :return: None or dict
        """
        if self._redis_client is None:
            raise NoConnectionError("Redis client not connected")
        if data := await self._redis_client.get(f"{key}"):
            return data
        return None

    async def _cache_delete_key(self, key: str) -> bool:
        """
        Delete key from Redis Cache
        :param key: Key Name
        :return: if operation was successful
        """
        if self._redis_client is None:
            raise NoConnectionError("Redis client not connected")
        if await self._redis_client.delete(key):
            return True
        else:
            return False
