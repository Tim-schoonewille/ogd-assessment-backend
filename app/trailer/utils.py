from typing import Any

from httpx import AsyncClient
from app.config import ConfigBase
from app.trailer.exceptions import MovieNotFoundError, OmdbApiError, YoutubeApiError
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
        return [models.CompactMovieData(**movie_data) for movie_data in data]

    def _convert_single_to_object(self, data: dict[str, Any]) -> MovieDataWithTrailer:
        """Converts the raw dictionary to a pydantic model."""
        return models.MovieDataWithTrailer(**data)


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
        async with AsyncClient() as c:
            result = await c.get(self._api_base_url, params=params)
            if result.status_code not in [200, 201, 202, 203, 204, 205]:
                raise YoutubeApiError(result.text)
            data = result.json()
        first_result = data['items'][0]
        return self._convert_to_object(data=first_result)

    def _convert_to_object(self, data: dict[str, Any]) -> YoutubeTrailerData:
        "Converts the raw dictionary JSON representation to a pydantic model."
        # TODO Test invalid input
        return YoutubeTrailerData(**data)
