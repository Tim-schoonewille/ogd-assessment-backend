import json
from httpx import AsyncClient


async def test_search_endpoint(mock_v2_fastapi: AsyncClient) -> None:
    QUERY = 'lord of the rings'
    FILEPATH = './tests/data/trailer/search-lotr.json'

    with open(FILEPATH, 'r', encoding='utf-8') as file:
        data_from_file = json.loads(file.read())

    body = {'title': QUERY}
    params = {'network_lag': 0}

    r = await mock_v2_fastapi.post('/trailer/search', json=body, params=params)

    assert r.status_code == 200

    data = r.json()

    for i, movie in enumerate(data_from_file):
        assert movie['Title'] == data[i]['title']
        assert movie['imdbID'] == data[i]['imdbid']


async def test_search_endpoint_movie_not_found(mock_v2_fastapi: AsyncClient) -> None:
    QUERY = 'the lord of the rings'

    body = {'title': QUERY}
    params = {'network_lag': 0}

    r = await mock_v2_fastapi.post('/trailer/search', json=body, params=params)

    assert r.status_code == 404
    assert r.json()['detail'] == 'MOVIE_NOT_FOUND'


async def test_search_by_imdb_id_endpoint(mock_v2_fastapi: AsyncClient) -> None:
    FILEPATH_SEARCH = './tests/data/trailer/search-lotr.json'
    FILEPATH_RESULT = './tests/data/trailer/trailer-result-lotr.json'

    with open(FILEPATH_SEARCH, 'r', encoding='utf-8') as f:
        search_data = json.loads(f.read())

    with open(FILEPATH_RESULT, 'r', encoding='utf-8') as f:
        result_data = json.loads(f.read())

    title = search_data[0]['Title']
    imdb_id = search_data[0]['imdbID']
    body = {'title': title}
    params = {'network_lag': 0}
    r = await mock_v2_fastapi.post(f'/trailer/search/{imdb_id}', json=body, params=params)

    assert r.status_code == 200

    data = r.json()
    assert data['title'] == title
    assert data['imdbid'] == imdb_id
    assert data['trailerLink']
    assert str(data['trailerLink']).startswith('https://')


async def test_search_by_imdb_id_endpoint_invalid_imdb_id(
    mock_v2_fastapi: AsyncClient,
) -> None:
    title = 'fuck this shit'
    imdb_id = 'non-existent-imdb-id'
    body = {'title': title}
    params = {'network_lag': 0}
    r = await mock_v2_fastapi.post(f'/trailer/search/{imdb_id}', json=body, params=params)

    assert r.status_code == 404
    assert r.json()['detail'] == 'INVALID_IMDB_ID'
