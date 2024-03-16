import json
import random
from fastapi import FastAPI, middleware
from httpx import ASGITransport, AsyncClient
from redis.asyncio import Redis as AsyncRedis
from app import models
from app.trailer.utils import CacheHeaderMiddleware


# def init_test_app(with_middleware: bool = False):
#     app = FastAPI()

#     if with_middleware:
#         app.add_middleware(CacheHeaderMiddleware)

#     @app.get('/')
#     def random_value():
#         return {'value': random.randint(0, 100000)}

#     @app.get('/api/v2/trailer/search')
#     def compact_data_list_endpoint(title: str):
#         return [{'title': title}]

#     return app


# async def test_cache_middleware_basic() -> None:
#     app_without_middleware = init_test_app()
#     async with AsyncClient(
#         base_url='http://localhost:8000',
#         transport=ASGITransport(app_without_middleware),  # type: ignore
#     ) as client:
#         r = await client.get('/')
#         assert 'Cache-Control' not in r.headers
#         random_value_response_without_cache_headers = r.json()['value']

#     app_with_middleware = init_test_app(with_middleware=True)

#     async with AsyncClient(
#         base_url='http://localhost:8000',
#         transport=ASGITransport(app_with_middleware),  # type: ignore
#     ) as client:
#         r = await client.get('/')
#         random_value_response_with_header_1 = r.json()['value']
#         r = await client.get('/')
#         random_value_response_with_header_2 = r.json()['value']
#         assert 'Cache-Control' in r.headers
#     return None


# async def test_cache_middleware_compact_movie_data(cache: AsyncRedis):
#     TITLE = 'STAR WARS'
#     cache_key = f'{models.CachePrefixes.COMPACT_MOVIE_DATA_LIST}{TITLE}'

#     await cache.set(cache_key, json.dumps({'foo': 'bar'}), ex=5000)
#     app = init_test_app(with_middleware=True)

#     async with AsyncClient(
#         base_url='http://localhost:8000',
#         transport=ASGITransport(app),  # type: ignore
#     ) as client:
#         params = {'title': TITLE}
#         r = await client.get('/api/v2/trailer/search', params=params)
#         cc_header = r.headers.get('cache-control')

#     assert cc_header != 'max-age=300'
#     # max_age = cc_header.split('=')[1]
#     max_age = cc_header.split(',')[1].strip().split('=')[1]
#     assert 4999 < int(max_age) < 5001


# async def test_cache_middleware_movie_data_with_trailer(cache: AsyncRedis):
#     ID = 'tt12313131'

#     cache_key = f'{models.CachePrefixes.SINGLE_RESULT_BY_ID}{ID}'

#     await cache.set(cache_key, json.dumps({'id': ID}), ex=7000)

#     app = init_test_app(with_middleware=True)

#     async with AsyncClient(
#         base_url='http://localhost:8000', transport=ASGITransport(app)
#     ) as client:
#         r = await client.get(f'/api/v2/trailer/search/{ID}')
#         cc_header = r.headers.get('cache-control')

#     assert cc_header != 'max-age=300'
#     print(cc_header)
#     # max_age = int(cc_header.split('=')[1])
#     max_age = int(cc_header.split(',')[1].strip().split('=')[1])
#     assert 6999 < max_age < 7001
