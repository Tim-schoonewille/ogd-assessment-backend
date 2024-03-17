import json

import pytest
from app import models
from app.config import get_config, ConfigBase
from app.trailer.exceptions import InvalidTrailerData, YoutubeApiError

from app.trailer.utils import YoutubeTrailerProvider


YOUTUBE_JSON_FILEPATH = './tests/data/trailer/youtube-mr_robot.json'


def test_convert_to_object():
    provider = YoutubeTrailerProvider(config=get_config())
    with open(YOUTUBE_JSON_FILEPATH, 'r', encoding='utf-8') as f:
        data = json.loads(f.read())

    result = provider._convert_to_object(data=data)

    assert isinstance(result, models.YoutubeTrailerData)

    assert result.id.videoId == data['id']['videoId']
    assert result.snippet.publishedAt == data['snippet']['publishedAt']
    assert result.snippet.channelId == data['snippet']['channelId']
    assert result.snippet.title == data['snippet']['title']
    assert result.snippet.description == data['snippet']['description']
    assert result.snippet.channelTitle == data['snippet']['channelTitle']


async def test_search_multi_return_one():
    provider = YoutubeTrailerProvider(config=get_config())
    with open(YOUTUBE_JSON_FILEPATH, 'r', encoding='utf-8') as f:
        data = json.loads(f.read())

    result = await provider.search_multi_return_first(title='mr robot')

    assert isinstance(result, models.YoutubeTrailerData)

    assert result.id.videoId == data['id']['videoId']
    assert result.snippet.publishedAt == data['snippet']['publishedAt']
    assert result.snippet.channelId == data['snippet']['channelId']
    assert result.snippet.title == data['snippet']['title']
    assert result.snippet.description == data['snippet']['description']
    assert result.snippet.channelTitle == data['snippet']['channelTitle']


async def test_search_multi_return_one_api_error(mock_config: ConfigBase) -> None:
    provider = YoutubeTrailerProvider(mock_config)
    with pytest.raises(YoutubeApiError):
        await provider.search_multi_return_first(title='foo')


def test_convert_to_object_invalid_data() -> None:
    provider = YoutubeTrailerProvider(get_config())
    invalid_data = {'foo': 'bar'}
    with pytest.raises(InvalidTrailerData):
        provider._convert_to_object(invalid_data)
