import logging
import os
from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.middlewares import CacheHeaderMiddleware
from app.trailer.routers.mock_router import router as mock_trailer_router
from app.trailer.routers.mock_router_v2 import router as v2_mock_trailer_router
from app.trailer.routers.router import router as trailer_router
from app.trailer.routers.router_v2 import router as v2_trailer_router
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
        version=os.environ.get('API_VERSION', 'unreleased'),
        lifespan=lifespan,
        generate_unique_id_function=custom_generate_unique_id,
    )

    origins = [
        'http://localhost',
        'http://localhost:3000',
        'http://localhost:5500',
        'http://localhost:3001',
    ]
    server.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )
    server.add_middleware(CacheHeaderMiddleware)

    api_v1 = APIRouter(prefix='/api/v1')
    mock_v1 = APIRouter(prefix='/mock/v1')
    api_v2 = APIRouter(prefix='/api/v2')
    mock_v2 = APIRouter(prefix='/mock/v2')

    api_v1.include_router(router=trailer_router)

    api_v2.include_router(router=v2_trailer_router)

    mock_v1.include_router(router=mock_trailer_router)

    mock_v2.include_router(router=v2_mock_trailer_router)

    server.include_router(router=api_v1)
    server.include_router(router=mock_v1)
    server.include_router(router=api_v2)
    server.include_router(router=mock_v2)

    return server


app = init_fastapi(testing=False)


@app.get('/health', tags=['health'])
def health_endpoint():
    return {'alive': True}
