from httpx import AsyncClient
import pytest_asyncio
from redis import asyncio as aioredis

from app.config import get_config
from app.main import init_fastapi

API_BASE_URL = 'http://localhost:8000/api/v1'


# @pytest_asyncio.fixture(scope='function')
# async def std_fastapi_client():
#     app = init_fastapi(testing=True)

#     async with AsyncClient(app=app, base_url=API_BASE_URL, follow_redirects=True) as c:
#         yield c


# @pytest_asyncio.fixture(scope='function')
# async def fastapi_trailer():
#     """Fastapi fixture for trailer service."""
#     app = init_fastapi(testing=True)

#     async with AsyncClient(app=app, base_url=API_BASE_URL, follow_redirects=True) as c:
#         yield c


@pytest_asyncio.fixture(scope='function')
async def cache():
    """Fixture to receive async redis cache client. Flushes the DB on every call."""
    config = get_config()
    url = 'redis://:REDIS_PASSWORD@cache/0:6379'
    redis = aioredis.from_url(url)
    await redis.execute_command('FLUSHALL ASYNC')
    async with redis.client() as c:
        yield c
        await c.aclose()
