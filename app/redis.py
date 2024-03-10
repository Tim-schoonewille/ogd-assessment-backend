from typing import Annotated, TypeAlias
from fastapi import Depends
from redis import asyncio as aioredis
from redis.asyncio import Redis as AsyncRedis

from app.config import get_config


config = get_config()

REDIS_URL = f'redis://:{config.REDIS_PASSWORD}@{config.REDIS_HOST}/0:6379'


async def get_cache():
    """Dependency for FastAPI endpoints."""
    redis = aioredis.from_url(url=REDIS_URL)
    async with redis.client() as client:
        yield client


GetAsyncCache: TypeAlias = Annotated[AsyncRedis, Depends(get_cache)]
