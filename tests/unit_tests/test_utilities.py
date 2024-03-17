from typing import Annotated
from fastapi import Depends, FastAPI
from fastapi.routing import APIRoute
from redis.asyncio import Redis as AsyncRedis
from app.redis import get_cache

from app.utilities import custom_generate_unique_id


def test_custom_route():
    route = APIRoute(
        endpoint=lambda: None, path='/test', tags=['test'], name='cool route'
    )
    print(route.name)
    print(route.tags)

    result = custom_generate_unique_id(route)

    assert result == 'test-cool route'


def test_custom_route_no_tags():
    route = APIRoute(endpoint=lambda: None, path='/api/test', name='cool route')

    result = custom_generate_unique_id(route)

    assert result == 'api-test-cool route'


async def test_get_cache():
    app = FastAPI()

    @app.get('/cache')
    async def route_with_cache(cache: Annotated[AsyncRedis, Depends(get_cache)]):
        assert type(cache) == 'Redis'
        return True
