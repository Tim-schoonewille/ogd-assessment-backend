import json
import pytest
from redis.asyncio import Redis as AsyncRedis
from app import models
from app.config import get_config
from app.trailer.exceptions import InvalidIMDBId

from app.utilities import CacheProvider
from tests.data.trailer.mock_utilities import MockTrailerService


async def test_mock_trailer_service(cache: AsyncRedis):
    cache_provider = CacheProvider(cache_client=cache)
    service = MockTrailerService(config=get_config(), cache_provider=cache_provider)

    for title in service.compact_movie_data_entries:
        for movie in service.compact_movie_data_entries[title]:
            assert movie.imdbID in service.movie_data_with_trailer_entries


async def test_mock_trailer_search(cache: AsyncRedis) -> None:
    QUERY = 'lord of the rings'
    FILEPATH = './tests/data/trailer/trailer-result-lotr.json'

    with open(FILEPATH, 'r', encoding='utf-8') as f:
        data = (json.loads(f.read()))['movies']

    cache_provider = CacheProvider(cache_client=cache)
    service = MockTrailerService(config=get_config(), cache_provider=cache_provider)

    result = await service.search(query=QUERY, network_lag=0)
    assert isinstance(result, models.TrailerResult)
    for i, movie in enumerate(result.movies):
        assert movie.Title == data[i]['Title']


async def test_get_movie_data_with_trailer_by_imdb_id(cache: AsyncRedis) -> None:
    FILEPATH_SEARCH = './tests/data/trailer/search-lotr.json'
    FILEPATH_RESULT = './tests/data/trailer/trailer-result-lotr.json'

    with open(FILEPATH_SEARCH, 'r', encoding='utf-8') as f:
        search_data = json.loads(f.read())

    with open(FILEPATH_RESULT, 'r', encoding='utf-8') as f:
        result_data = json.loads(f.read())

    cache_provider = CacheProvider(cache_client=cache)
    service = MockTrailerService(config=get_config(), cache_provider=cache_provider)

    title = search_data[0]['Title']
    imdb_id = search_data[0]['imdbID']

    movie_data_with_trailer = await service.get_movie_data_with_trailer_by_imdb_id(
        _id=imdb_id, network_lag=0
    )
    assert isinstance(movie_data_with_trailer, models.MovieDataWithTrailer)
    assert movie_data_with_trailer.Title == title
    assert movie_data_with_trailer.trailer_link
    assert movie_data_with_trailer.trailer_link.startswith(
        'https://www.youtube.com/watch?v='
    )
    assert movie_data_with_trailer.trailer_embed_link
    assert movie_data_with_trailer.trailer_embed_link.startswith(
        'https://www.youtube.com/embed/'
    )
    assert movie_data_with_trailer.imdbID == imdb_id


async def test_get_movie_data_with_trailer_by_imdb_id_invalid_id(
    cache: AsyncRedis,
) -> None:
    cache_provider = CacheProvider(cache_client=cache)
    service = MockTrailerService(config=get_config(), cache_provider=cache_provider)

    with pytest.raises(InvalidIMDBId):
        await service.get_movie_data_with_trailer_by_imdb_id(_id='asdfsad', network_lag=0)


async def test_get_compact_movie_data_by_query(cache: AsyncRedis) -> None:
    FILEPATH_SEARCH = './tests/data/trailer/search-lotr.json'
    with open(FILEPATH_SEARCH, 'r', encoding='utf-8') as f:
        search_data = json.loads(f.read())

    cache_provider = CacheProvider(cache_client=cache)
    service = MockTrailerService(config=get_config(), cache_provider=cache_provider)

    compact_movie_data = await service.get_compact_movie_data_by_query(
        'lord of the rings', network_lag=0
    )

    for i, movie_data in enumerate(compact_movie_data):
        assert isinstance(movie_data, models.CompactMovieData)
        assert movie_data.Title == search_data[i]['Title']
        assert movie_data.imdbID == search_data[i]['imdbID']
