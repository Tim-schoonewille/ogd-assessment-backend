import json
from typing import Any

from fastapi.routing import APIRoute

from app.interfaces import ICacheProvider
from redis.asyncio import Redis as AsyncRedis


def custom_generate_unique_id(route: APIRoute) -> str:
    """Generate custom unique id function for fastapi docs/client creation."""
    try:
        unique_id = f'{route.tags[0]}-{route.name}'
    except IndexError:
        path_split = route.path.split('/')
        path_joined_with_dash = '-'.join(path_split)
        unique_id = (f'{path_joined_with_dash}-{route.name}')[1:]
    return unique_id


class CacheProvider(ICacheProvider):
    """Creates an object for our caching mechanism."""

    def __init__(self, cache_client: AsyncRedis, cache_expire: int = 3600) -> None:
        self.cache_client = cache_client
        self.cache_expire = cache_expire

    async def get_str(self, key: str) -> str | None:
        """Returns a string from cache.

        Args:
            key (str): The key associated with the cached entry.

        Returns:
            str: The value associated with the cached entry.
        """
        value = await self.cache_client.get(name=key)
        return value.decode() if value else None

    async def get_json(self, key: str) -> dict[str, Any] | None:
        """Returns a dictionary object represneting JSON data from cache.

        Args:
            key (str): The key associated with the cached entry.

        Returns:
            dict[str, Any]: A dictionary representing the JSON data.
        """

        value = await self.cache_client.get(name=key)
        return json.loads(value) if value else None

    async def store_str(self, key: str, value: str) -> None:
        """Store string data in cache.

        Args:
            key (str): Key to associate data in cache.
            value (str): Value of the data to be stored in cache.

        Returns:
            None
        """

        await self.cache_client.set(name=key, value=value, ex=self.cache_expire)

    async def store_json(self, key: str, value: dict[str, Any]) -> None:
        """Store JSON data in cache.

        Args:
            key (str): Key to associate data in cache.
            value (dict[str, Any]): Represnetation of JSON data to be stored in cache.

        Returns:
            None

        Returns:
            None
        """
        await self.cache_client.set(
            name=key, value=json.dumps(value), ex=self.cache_expire
        )