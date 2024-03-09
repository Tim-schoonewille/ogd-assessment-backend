import json
from httpx import AsyncClient


async def test_search_endpoint(trailer_v1_fastapi: AsyncClient) -> None:
    QUERY = 'lord of the rings'
    FILEPATH = './tests/data/trailer/trailer-result-lotr.json'

    with open(FILEPATH, 'r', encoding='utf-8') as file:
        data_from_file = (json.loads(file.read()))['movies']

    body = {'title': QUERY}
    r = await trailer_v1_fastapi.post('/trailer/search', json=body)

    assert r.status_code == 200

    data = r.json()
    movies_from_result = data['movies']

    for i, movie in enumerate(movies_from_result):
        assert movie['title'] == data_from_file[i]['Title']


async def test_search_endpoint_invalid_title(trailer_v1_fastapi: AsyncClient) -> None:
    QUERY = 'the lord of the rings'

    body = {'title': QUERY}
    r = await trailer_v1_fastapi.post('/trailer/search', json=body)

    assert r.status_code == 404
