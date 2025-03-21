import os
from typing import Annotated
from fastapi import Depends, FastAPI
from httpx import ASGITransport, AsyncClient
import pytest
from _pytest.logging import LogCaptureFixture

from app.config import ConfigBase
from app.interfaces import ICacheProvider
from app.main import init_fastapi, lifespan, app as initiated_app
from app.trailer.dependencies import get_trailer_service
from app.trailer.interfaces import IMovieDataProvider, ITrailerProvider
from app.trailer.service import TrailerService


@pytest.mark.asyncio
async def test_lifespan(captured_logs: LogCaptureFixture):
    app = init_fastapi(testing=True)
    async with lifespan(app):
        pass

    assert '[+] Setting up application..' in captured_logs.text
    assert '[+] Tearing down application..' in captured_logs.text


async def test_init_fastapi() -> None:
    routes = [
        '/api/v1/trailer/search',
        '/api/v2/trailer/search',
        '/api/v2/trailer/search/{imdb_id}',
        '/mock/v1/trailer/search',
        '/mock/v2/trailer/search',
        '/mock/v2/trailer/search/{imdb_id}',
    ]
    app = init_fastapi()

    assert isinstance(app, FastAPI)
    assert app.title == os.environ.get('APP_TITLE')
    assert app.version == os.environ.get('API_VERSION')

    api_routes = [route.path for route in app.routes]  # type: ignore
    for route in routes:
        assert route in api_routes


async def test_health_endpoint():
    async with AsyncClient(
        transport=ASGITransport(initiated_app),  # type: ignore
        base_url='http://localhost:8000/',
    ) as client:
        r = await client.get('health')
        assert r.status_code == 200
        assert r.json()['alive'] is True


async def test_trailer_service_dependency():
    app = FastAPI()

    @app.get('/')
    async def trailer_service(
        service: Annotated[TrailerService, Depends(get_trailer_service)],
    ):
        assert isinstance(service._config, ConfigBase)
        assert isinstance(service._cache_provider, ICacheProvider)
        assert isinstance(service._movie_provider, IMovieDataProvider)
        assert isinstance(service._trailer_provider, ITrailerProvider)
        return True

