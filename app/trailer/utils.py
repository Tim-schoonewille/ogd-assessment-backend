import json
from typing import Annotated, Any

from fastapi import Depends, Request, responses
from httpx import AsyncClient, ConnectTimeout
from redis.asyncio import Redis as AsyncRedis
from redis import asyncio as aioredis
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from pydantic import ValidationError
from starlette.responses import Response
from app.config import ConfigBase, get_config
from app.trailer.exceptions import (
    InvalidIMDBId,
    InvalidTrailerData,
    MovieNotFoundError,
    OmdbApiError,
    YoutubeApiError,
)
from app.trailer.interfaces import IMovieDataProvider, ITrailerProvider
from app import models
from app.trailer.models import MovieDataWithTrailer, YoutubeTrailerData


class OMDBMovieDataProvider(IMovieDataProvider):
    """
    Provider object to get data from the external api.
    The Api is: OMDB (https://www.omdbapi.com/)

    Args:
        config (ConfigBase) -- The global configuration object with settings.
    """

    def __init__(self, config: ConfigBase) -> None:
        self._config = config
        self._api_base_url = self._config.OMDB_API_URL
        self._api_key = self._config.OMDB_API_KEY

    async def search_multi(self, query: str) -> list[models.CompactMovieData]:
        """
        Search external API for movies.

        Args:
            query (str) -- The movie to search

        Returns:
            list[CompactMovieData] -- A list of pydantic models with data from api.
        """
        # TODO httpx is timing out for some reason.
        async with AsyncClient(timeout=20) as c:
            params = {'apikey': self._api_key, 's': query.strip()}
            result = await c.get(self._api_base_url, params=params)

            if result.status_code not in [200, 201, 202, 203, 204]:
                raise OmdbApiError('OMDB_API_ERROR: ', result.text)

            data = result.json()

        try:
            search_data = data['Search']
        except KeyError:
            raise MovieNotFoundError('MOVIE_NOT_FOUND')

        return self._convert_multi_to_object(data=search_data)

    async def get_by_id(self, _id: str) -> models.MovieDataWithTrailer:
        """
        Search external API by imdb ID.

        Args:
            _id (str) -- The IMDB movie ID.

        Returns:
            MovieData -- A pydantic model with complete data from the API.

        """
        async with AsyncClient() as c:
            params = {'apikey': self._api_key, 'i': _id.strip()}
            result = await c.get(self._api_base_url, params=params)

            if result.status_code not in [200, 201, 202, 203, 204]:
                raise OmdbApiError('OMDB_API_ERROR: ', result.text)

            data = result.json()

        return self._convert_single_to_object(data=data)

    def _convert_multi_to_object(
        self, data: list[dict[str, str]]
    ) -> list[models.CompactMovieData]:
        """Converts the raw list of dictionaries to pydantic models."""
        try:
            converted_objects = [
                models.CompactMovieData(**movie_data) for movie_data in data
            ]
        except ValidationError:
            raise MovieNotFoundError('MOVIE_NOT_FOUND')
        return converted_objects

    def _convert_single_to_object(self, data: dict[str, Any]) -> MovieDataWithTrailer:
        """Converts the raw dictionary to a pydantic model."""
        try:
            converted_object = models.MovieDataWithTrailer(**data)
        except ValidationError:
            raise InvalidIMDBId('INVALID_IMDB_ID')
        return converted_object


class YoutubeTrailerProvider(ITrailerProvider):
    """
    Provider object to get a trailer from the YouTube API.
    api url: ('https://www.googleapis.com/youtube/v3/search')

    Args:
        config (ConfigBase) -- Global configuration object.
    """

    def __init__(self, config: ConfigBase) -> None:
        self._config = config
        self._api_key = config.YOUTUBE_API_KEY
        self._api_base_url = config.YOUTUBE_API_URL

    async def search_multi_return_first(self, title: str) -> YoutubeTrailerData:
        """
        Searches the Youtube API endpoint for a list of movie trailers.
        The 'query' argument is stripped of any whitespace etc, and concatenated with
        'trailer'.
        Currently, returns the first value of the list.

        Args:
            query (str) -- This is the movie title.

        Returns:
            YoutubeTrailerData -- Pydantic model with some metadata, but the most
            important value is: YoutubeTrailerData.id.videoId, for this is the
            id of the trailer (add to: /watch?v={videoId})
        """
        params = {
            'part': 'snippet',
            'q': f'{title.strip()} trailer',
            'key': self._api_key,
        }

        try:
            async with AsyncClient(timeout=20) as c:
                result = await c.get(self._api_base_url, params=params)

                if result.status_code not in [200, 201, 202, 203, 204, 205]:
                    raise YoutubeApiError(result.text)

                data = result.json()

            first_result = data['items'][0]

        except ConnectTimeout:
            raise YoutubeApiError('EXTERNAL_API_ERROR')

        return self._convert_to_object(data=first_result)

    def _convert_to_object(self, data: dict[str, Any]) -> YoutubeTrailerData:
        "Converts the raw dictionary JSON representation to a pydantic model."
        # TODO Test invalid input

        try:
            converted = YoutubeTrailerData(**data)
        except ValidationError:
            raise InvalidTrailerData('INVALID_TRAILER_DATA')
        return converted


def hello_dependency() -> str:
    return 'hello'


class CacheHeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        config = get_config()
        PATH = 'search'
        REDIS_URL = f'redis://:{config.REDIS_PASSWORD}@{config.REDIS_HOST}/0:6379'
        redis = aioredis.from_url(url=REDIS_URL)

        response = await call_next(request)
        response.headers.update({'Cache-Control': 'max-age=300'})

        path_parameters = request.url.path.split('/')
        query_parameters = request.query_params
        print('from middleware! :D')
        if PATH in path_parameters:
            path_index = path_parameters.index(PATH)
            title_param = query_parameters.get('title')
            if title_param is not None:
                print('we here!!')
                async with redis.client() as client:
                    cache_key = f'{models.CachePrefixes.COMPACT_MOVIE_DATA_LIST}{title_param.strip()}'
                    ttl = await client.ttl(cache_key)
                    response.headers['Cache-Control'] = (
                        f'public, max-age={ttl if ttl > 0 else 300}'
                    )
                    # This is too test:
                    # TODO Remove this
                    # response.headers['Cache-Control'] = 'public, max-age=30'

            else:
                try:
                    imdb_id = str(path_parameters[path_index + 1])
                    if imdb_id.startswith('tt'):
                        async with redis.client() as client:
                            cache_key = (
                                f'{models.CachePrefixes.SINGLE_RESULT_BY_ID}{imdb_id}'
                            )
                            ttl = await client.ttl(cache_key)
                            response.headers['Cache-Control'] = (
                                f'public, max-age={ttl if ttl > 0 else 300}'
                            )
                            # this is to test:
                            # TODO Remove this.
                            # response.headers['Cache-Control'] = 'public, max-age=30'

                except IndexError:
                    pass
        return response

        # TODO Test this!!!


async def get_max_age_of_movie_with_details_and_trailer(
    request: Request, cache: AsyncRedis
) -> int:
    PATH = 'search'
    path_parameters = request.url.path.split('/')

    if PATH in path_parameters:
        path_index = path_parameters.index(PATH)
        imdb_id = path_parameters[path_index + 1]
        if str(imdb_id).startswith('tt'):
            ttl = await cache.ttl(
                name=f'{models.CachePrefixes.SINGLE_RESULT_BY_ID}{imdb_id}'
            )
            return int(ttl)
    return 0


async def get_max_age_compact_movie_list(request: Request):
    pass
