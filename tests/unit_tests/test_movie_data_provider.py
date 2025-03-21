import json

import pytest
from app import models
from app.config import get_config, ConfigBase
from app.trailer.exceptions import InvalidIMDBId, MovieNotFoundError, OmdbApiError
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


def test_convert_multi_to_object_invalid_data():
    provider = OMDBMovieDataProvider(config=get_config())

    with pytest.raises(MovieNotFoundError):
        provider._convert_multi_to_object(data=[{'not-the-data': 'i would expect'}])


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


async def test_search_multi_movie_not_found():
    provider = OMDBMovieDataProvider(config=get_config())

    with pytest.raises(MovieNotFoundError):
        await provider.search_multi(query='#@)!$!_@#!@$!@$$')


async def test_search_multi_api_error(mock_config: ConfigBase):
    provider = OMDBMovieDataProvider(config=mock_config)
    with pytest.raises(OmdbApiError):
        await provider.search_multi(query='star wars')


def test_convert_single_to_object():
    provider = OMDBMovieDataProvider(config=get_config())
    with open(FULL_MOVIE_DATA_FILEPATH, 'r', encoding='utf-8') as f:
        data = json.loads(f.read())

    result = provider._convert_single_to_object(data=data)
    assert isinstance(result, models.MovieDataWithTrailer)


def test_convert_single_to_object_invalid_data():
    provider = OMDBMovieDataProvider(config=get_config())

    with pytest.raises(InvalidIMDBId):
        provider._convert_single_to_object(data={'not-the-data': 'i expected'})


async def test_search_by_id():
    provider = OMDBMovieDataProvider(config=get_config())
    with open(FULL_MOVIE_DATA_FILEPATH, 'r', encoding='utf-8') as f:
        data = json.loads(f.read())

    result = await provider.get_by_id('tt0120915')

    print('result from get by id: ', result)
    for k, v in data.items():
        if hasattr(result, k):
            assert data[k] == getattr(result, k)


async def test_search_by_id_api_error(mock_config: ConfigBase):
    provider = OMDBMovieDataProvider(mock_config)

    with pytest.raises(OmdbApiError):
        await provider.get_by_id(_id='rofl')


# TODO Test raise for status.


# async def test_search_multi_for_output():
#     provider = OMDBMovieDataProvider(config=get_config())

#     QUERY = 'indiana jones'
#     FILEPATH = './tests/data/trailer/search-indiana-jones.json'

#     result = await provider.search_multi(query=QUERY)
#     print('result from search multi:', result)

#     with open(FILEPATH, 'w', encoding='utf-8') as f:
#         f.write(json.dumps([movie.model_dump() for movie in result]))
