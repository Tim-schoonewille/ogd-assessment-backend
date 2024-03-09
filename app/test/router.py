import json
from typing import Annotated
from fastapi import APIRouter, Depends
from httpx import AsyncClient

from redis import asyncio as aioredis
from redis import Redis

from app.config import ConfigBase, get_config

router = APIRouter(prefix='/test', tags=['tests'])


@router.get('/')
def test_route():
    return {'hello': 'world'}


@router.post('/cache')
def post_cache(k: str, v: str):
    redis = Redis(host='cache', port=6379, password='REDIS_PASSWORD')

    redis.set(k, v, ex=3600)
    return True


@router.get('/test-vimeo-tutorial')
async def get_video(config: Annotated[ConfigBase, Depends(get_config)]) -> dict[str, str]:
    async with AsyncClient() as client:
        headers = {'Authorization': f'bearer {config.VIMEO_API_KEY}'}
        r = await client.get('https://api.vimeo.com/tutorial', headers=headers)

        response_text = r.text
        print('status code:', r.status_code)
        print('response test:', response_text)

    return {'res:': response_text}


@router.get('/vimeo-get-video')
async def get_vimeo_trailer(
    title: str, config: Annotated[ConfigBase, Depends(get_config)]
):
    url = 'https://api.vimeo.com/videos'
    async with AsyncClient() as c:
        params = {'query': f'{title.strip()} official release trailer'}
        headers = {'Authorization': f'bearer {config.VIMEO_API_KEY}'}

        r = await c.get(url, params=params, headers=headers, timeout=20)

        full_response = r.json()
        trailer_link = full_response['data'][0]['link']
        for movie in full_response['data']:
            if 'official' in movie['name'].lower():
                trailer_link = movie['link']
                break

        # with open('./vimeo-response.json', 'w', encoding='utf-8') as f:
        #     f.write(json.dumps(full_response))

    print(full_response)
    return {f'{title} trailer': trailer_link}
