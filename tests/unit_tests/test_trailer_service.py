import json

from redis.asyncio import Redis as AsyncRedis

from app import models
from app.trailer.service import TrailerService

STARWARS_SEARCH_JSON_FILEPATH = './tests/data/trailer/search-star-wars.json'

TRAILER_RESULT_FILEPATH = './tests/data/trailer/trailer-result-starwars.json'


async def test_trailer_service(
    trailer_service: TrailerService,
) -> None:
    QUERY = 'star wars'

    with open(STARWARS_SEARCH_JSON_FILEPATH, 'r', encoding='utf-8') as f:
        data = json.loads(f.read())['Search']

    result = await trailer_service._search_movies_with_trailers(query=QUERY)

    assert isinstance(result, models.TrailerResult)
    assert result.from_cache is False

    for movie in result.movies:
        print('movie title: ', movie.Title)
        print('youtube link:', movie.trailer_link)

    for i, value in enumerate(data):
        assert value['Title'] == result.movies[i].Title

    with open(TRAILER_RESULT_FILEPATH, 'w', encoding='utf-8') as f:
        f.write(result.model_dump_json())


async def test_trailer_service_test_result_is_cached(
    trailer_service: TrailerService, cache: AsyncRedis
) -> None:
    QUERY = 'under the silver lake'
    result_in_cache_before = await cache.get(
        name=f'{models.CachePrefixes.FULL_RESULT}{QUERY}'
    )
    assert result_in_cache_before is None

    result = await trailer_service.search(query=QUERY)

    for movie in result.movies:
        print('movie title: ', movie.Title)
        print('youtube link:', movie.trailer_link)

    result_in_cache_after = await cache.get(
        name=f'{models.CachePrefixes.FULL_RESULT}{QUERY}'
    )
    assert result_in_cache_after is not None


async def test_get_trailer_result_from_cache(
    trailer_service: TrailerService, cache: AsyncRedis
) -> None:
    with open(TRAILER_RESULT_FILEPATH, 'r', encoding='utf-8') as f:
        data = json.loads(f.read())

    await cache.set(
        name=f'{models.CachePrefixes.FULL_RESULT}star wars',
        value=json.dumps(data),
        ex=3600,
    )

    trailer_result = await trailer_service.search(query='star wars')
    assert trailer_result.from_cache is True
