from fastapi import APIRouter

from redis import asyncio as aioredis
from redis import Redis

router = APIRouter(prefix='/test', tags=['tests'])


@router.get('/')
def test_route():
    return {'hello': 'world'}


@router.post('/cache')
def post_cache(k: str, v: str):
    redis = Redis(host='cache', port=6379, password='REDIS_PASSWORD')

    redis.set(k, v, ex=3600)
    return True
