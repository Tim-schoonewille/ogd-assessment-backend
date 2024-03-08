from httpx import AsyncClient
import pytest_asyncio

from app.main import init_fastapi

API_BASE_URL = 'http://localhost:8000/api/v1'


@pytest_asyncio.fixture(scope='function')
async def std_fastapi_client():
    app = init_fastapi(testing=True)

    async with AsyncClient(app=app, base_url=API_BASE_URL, follow_redirects=True) as c:
        yield c


@pytest_asyncio.fixture(scope='function')
async def fastapi_trailer():
    """Fastapi fixture for trailer service."""
    app = init_fastapi(testing=True)

    async with AsyncClient(app=app, base_url=API_BASE_URL, follow_redirects=True) as c:
        yield c
