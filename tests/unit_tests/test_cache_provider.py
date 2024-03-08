import json
from redis import asyncio as aioredis
from redis.asyncio import Redis as AsyncRedis

from app.utilities import CacheProvider


TEST_STR_KEY = 'TEST'
TEST_STR_VALUE = 'ogd-is-the-best'

TEST_JSON_KEY = 'JSON_TEST'
TEST_JSON_VALUE = {'foo': 'shmoo', 'bar': 'sjmar'}


async def test_cache_store_str(cache: AsyncRedis) -> None:
    """Test the 'set_str' method of the cache provider."""
    print('rofl')
    value_in_cache_before = await cache.get(name=TEST_STR_KEY)
    assert value_in_cache_before is None

    cache_provider = CacheProvider(cache_client=cache)
    await cache_provider.store_str(key=TEST_STR_KEY, value=TEST_STR_VALUE)

    value_in_cache_after = (await cache.get(name=TEST_STR_KEY)).decode()
    assert value_in_cache_after is not None
    assert value_in_cache_after == TEST_STR_VALUE


async def test_cache_store_json(cache: AsyncRedis) -> None:
    """Test the store_json method from the cache provider."""

    value_in_cache_before = await cache.get(name=TEST_JSON_KEY)
    assert value_in_cache_before is None

    cache_provider = CacheProvider(cache_client=cache)
    await cache_provider.store_json(key=TEST_JSON_KEY, value=TEST_JSON_VALUE)

    value_in_cache_after = json.loads(await cache.get(name=TEST_JSON_KEY))
    assert value_in_cache_after is not None
    assert value_in_cache_after['foo'] == TEST_JSON_VALUE['foo']
    assert value_in_cache_after['bar'] == TEST_JSON_VALUE['bar']


async def test_cache_get_str(cache: AsyncRedis) -> None:
    """Test 'get_str' method from cache provider."""

    await cache.set(name=TEST_STR_KEY, value=TEST_STR_VALUE, ex=360)

    cache_provider = CacheProvider(cache)
    value_from_cache = await cache_provider.get_str(key=TEST_STR_KEY)

    assert value_from_cache
    assert value_from_cache == TEST_STR_VALUE


async def test_cache_get_json(cache: AsyncRedis) -> None:
    """Test 'get_json' method from cache provider"""

    await cache.set(name=TEST_JSON_KEY, value=json.dumps(TEST_JSON_VALUE), ex=360)

    cache_provider = CacheProvider(cache)
    value_from_cache = await cache_provider.get_json(key=TEST_JSON_KEY)
    assert value_from_cache
    assert value_from_cache['foo'] == TEST_JSON_VALUE['foo']
    assert value_from_cache['bar'] == TEST_JSON_VALUE['bar']
