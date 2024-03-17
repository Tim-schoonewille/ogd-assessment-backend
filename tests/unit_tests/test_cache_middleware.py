from hashlib import md5
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from app.middlewares import CacheHeaderMiddleware


def init_test_app(with_middleware: bool = False):
    app = FastAPI()

    if with_middleware:
        app.add_middleware(CacheHeaderMiddleware)

    @app.get('/')
    def root():
        return {'key': 'value'}

    return app


async def test_cache_middleware() -> None:
    app_without_middleware = init_test_app()
    async with AsyncClient(
        base_url='http://localhost:8000',
        transport=ASGITransport(app_without_middleware),  # type: ignore
    ) as client:
        r = await client.get('/')
        assert 'Cache-Control' not in r.headers
        assert 'ETag' not in r.headers

    app_with_middleware = init_test_app(with_middleware=True)
    async with AsyncClient(
        base_url='http://localhost:8000',
        transport=ASGITransport(app_with_middleware),  # type: ignore
    ) as client:
        r = await client.get('/')
        assert 'Cache-Control' in r.headers
        assert 'ETag' in r.headers

        etag = md5(r.text.encode()).hexdigest()
        headers = {'If-None-Match': etag}
        r = await client.get('/', headers=headers)
        assert r.status_code == 304

