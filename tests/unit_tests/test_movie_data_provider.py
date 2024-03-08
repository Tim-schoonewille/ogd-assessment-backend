import json
from app import models
from app.config import get_config
from app.trailer.utils import OMDBMovieDataProvider


SEARCH_JSON_FILEPATH = './tests/data/trailer/search-star-wars.json'
FULL_MOVIE_DATA_FILEPATH = './tests/data/trailer/star-wars-I.json'


def test_convert_multi_to_object():
    provider = OMDBMovieDataProvider(config=get_config())
    with open(SEARCH_JSON_FILEPATH, 'r', encoding='utf-8') as f:
        data = json.loads(f.read())

    result = provider._convert_multi_to_object(data=data['Search'])
    for obj in result:
        assert isinstance(obj, models.CompactMovieData)


async def test_search_multi():
    provider = OMDBMovieDataProvider(config=get_config())

    with open(SEARCH_JSON_FILEPATH, 'r', encoding='utf-8') as f:
        data = json.loads(f.read())

    result = await provider.search_multi(query='star wars')
    print('result from search multi:', result)
    for obj in result:
        assert isinstance(obj, models.CompactMovieData)

    for i, value in enumerate(data['Search']):
        assert value['Title'] == result[i].Title
        assert value['Year'] == result[i].Year
        assert value['imdbID'] == result[i].imdbID
        assert value['Type'] == result[i].Type


def test_convert_single_to_object():
    provider = OMDBMovieDataProvider(config=get_config())
    with open(FULL_MOVIE_DATA_FILEPATH, 'r', encoding='utf-8') as f:
        data = json.loads(f.read())

    result = provider._convert_single_to_object(data=data)
    assert isinstance(result, models.MovieData)


async def test_search_by_id():
    provider = OMDBMovieDataProvider(config=get_config())
    with open(FULL_MOVIE_DATA_FILEPATH, 'r', encoding='utf-8') as f:
        data = json.loads(f.read())

    result = await provider.get_by_id('tt0120915')

    print('result from get by id: ', result)
    for k, v in data.items():
        if hasattr(result, k):
            assert data[k] == getattr(result, k)


# TODO Test raise for status.
