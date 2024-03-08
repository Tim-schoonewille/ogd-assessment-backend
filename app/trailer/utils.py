from typing import Any

from httpx import AsyncClient
from app.config import ConfigBase, get_config
from app.trailer.exceptions import OmdbApiError
from app.trailer.interfaces import IMovieDataProvider
from app import models
from app.trailer.models import MovieData


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
        async with AsyncClient() as c:
            params = {'apikey': self._api_key, 's': query.strip()}
            result = await c.get(self._api_base_url, params=params)
            if result.status_code not in [200, 201, 202, 203, 204]:
                raise OmdbApiError('OMDB_API_ERROR: ', result.text)
            data = result.json()

        return self._convert_multi_to_object(data=data['Search'])

    async def get_by_id(self, _id: str) -> models.MovieData:
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

    def _convert_single_to_object(self, data: dict[str, Any]) -> MovieData:
        """Converts the raw dictionary to a pydantic model."""
        return models.MovieData(**data)
