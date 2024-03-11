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

    for i, value in enumerate(data):
        assert value['Title'] == result.movies[i].Title

    # with open(TRAILER_RESULT_FILEPATH, 'w', encoding='utf-8') as f:
    #     f.write(result.model_dump_json())


async def test_trailer_service_test_result_is_cached(
    trailer_service: TrailerService, cache: AsyncRedis
) -> None:
    QUERY = 'under the silver lake'
    result_in_cache_before = await cache.get(
        name=f'{models.CachePrefixes.FULL_RESULT}{QUERY}'
    )
    assert result_in_cache_before is None

    result = await trailer_service.search(query=QUERY)

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


async def test_get_movie_data_with_trailer_by_imdb_id(
    trailer_service: TrailerService, cache: AsyncRedis
) -> None:
    with open(TRAILER_RESULT_FILEPATH, 'r', encoding='utf-8') as file:
        data = json.loads(file.read())

    first_result = data['movies'][0]

    imdb_id = first_result['imdbID']
    title = first_result['Title']

    cache_key = f'{models.CachePrefixes.SINGLE_RESULT_BY_ID}{imdb_id}'
    movie_data_with_trailer_before = await cache.get(cache_key)
    assert movie_data_with_trailer_before is None

    movie_data_with_trailer = (
        await trailer_service.get_movie_data_with_trailer_by_imdb_id(
            _id=imdb_id, title=title
        )
    )
    assert isinstance(movie_data_with_trailer, models.MovieDataWithTrailer)
    for k in first_result:
        print(k)
        if hasattr(movie_data_with_trailer, k):
            assert first_result[k] == getattr(movie_data_with_trailer, k)

    movie_data_with_trailer_after = json.loads(await cache.get(cache_key))
    assert movie_data_with_trailer_after is not None
    print(movie_data_with_trailer_after)
    for k in first_result:
        assert first_result[k] == movie_data_with_trailer_after[k]


async def test_get_compact_movie_data_by_query(
    trailer_service: TrailerService, cache: AsyncRedis
) -> None:
    QUERY = 'star wars'

    cache_key = f'{models.CachePrefixes.COMPACT_MOVIE_DATA_LIST}{QUERY}'
    data_in_cache_before = await cache.get(name=cache_key)
    assert data_in_cache_before is None

    with open(STARWARS_SEARCH_JSON_FILEPATH, 'r', encoding='utf-8') as f:
        data = json.loads(f.read())

    result = await trailer_service.get_compact_movie_data_by_query(query=QUERY)
    for obj in result:
        assert isinstance(obj, models.CompactMovieData)

    for i, value in enumerate(data['Search']):
        assert value['Title'] == result[i].Title
        assert value['Year'] == result[i].Year
        assert value['imdbID'] == result[i].imdbID
        assert value['Type'] == result[i].Type

    data_in_cache_after = json.loads(await cache.get(name=cache_key))
    assert data_in_cache_after is not None
    for i, value in enumerate(data_in_cache_after):
        assert value['Title'] == result[i].Title
        assert value['Year'] == result[i].Year
        assert value['imdbID'] == result[i].imdbID
        assert value['Type'] == result[i].Type


# async def test_trailer_service_for_output(
#     trailer_service: TrailerService,
# ) -> None:
#     QUERY = 'indiana jones'
#     FILEPATH = './tests/data/trailer/trailer-result-indiana-jones.json'

#     result = await trailer_service._search_movies_with_trailers(query=QUERY)

#     assert isinstance(result, models.TrailerResult)
#     assert result.from_cache is False

#     for movie in result.movies:
#         print('movie title: ', movie.Title)
#         print('youtube link:', movie.trailer_link)

#     with open(FILEPATH, 'w', encoding='utf-8') as f:
#         f.write(result.model_dump_json())

#     assert 1 == 0


async def test_validate_cached_compact_movie_data(trailer_service: TrailerService):
    mock_result_from_cache = [
        {
            'Title': 'test',
            'Year': '1991',
            'imdbID': 'tt_test_id',
            'Type': 'test',
            'Poster': 'poster',
        }
        for _ in range(0, 10)
    ]

    assert trailer_service._validate_cached_compact_movie_data(
        list_compact_movie_data=mock_result_from_cache
    )


async def test_validate_cached_movie_data_with_trailer(
    trailer_service: TrailerService,
) -> None:
    with open(TRAILER_RESULT_FILEPATH, 'r', encoding='utf-8') as f:
        mock_data_from_cache = (json.loads(f.read()))['movies'][0]

    assert trailer_service._validate_cached_movie_data_with_trailer(
        movie_data_with_trailer=mock_data_from_cache
    )
