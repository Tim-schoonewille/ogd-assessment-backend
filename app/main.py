from contextlib import asynccontextmanager
import logging
import os
from fastapi import APIRouter, FastAPI

from app.utilities import custom_generate_unique_id


log = logging.getLogger('uvicorn')


@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info('[+] Setting up application..')
    yield
    log.info('[+] Tearing down application..')


def init_fastapi(testing: bool = False) -> FastAPI:
    server = FastAPI(
        title=os.environ.get('APP_TITLE', 'backend'),
        version='0.1',
        lifespan=lifespan,
        generate_unique_id_function=custom_generate_unique_id,
    )

    api_v1 = APIRouter(prefix='/api/v1')
    mock_v1 = APIRouter(prefix='/mock/v1')
    api_v2 = APIRouter(prefix='/api/v2')
    mock_v2 = APIRouter(prefix='/mock/v2')

    from app.test.router import router as test_router
    from app.trailer.router import router as trailer_router

    api_v1.include_router(router=test_router)
    api_v1.include_router(router=trailer_router)

    from app.trailer.mock_router import router as mock_trailer_router

    mock_v1.include_router(mock_trailer_router)

    from app.trailer.mock_router_v2 import router as v2_mock_trailer_router

    mock_v2.include_router(v2_mock_trailer_router)

    server.include_router(api_v1)
    server.include_router(mock_v1)
    server.include_router(api_v2)
    server.include_router(mock_v2)

    return server


app = init_fastapi(testing=False)


@app.get('/health', tags=['health'])
def health_endpoint():
    return {'alive': True}
