import asyncio
from enum import Enum
import json
from app import models
from app.config import ConfigBase
from app.interfaces import ICacheProvider
from app.trailer.exceptions import InvalidIMDBId, MovieNotFoundError
from app.trailer.interfaces import ITrailerService
from app.trailer.models import (
    CompactMovieData,
    MovieDataWithTrailer,
    TrailerResult,
)


class MockMovies(str, Enum):
    STAR_WARS = 'star wars'
    LOTR = 'lord of the rings'
    INDIANA_JONES = 'indiana jones'


class MockTrailerSearchForm(models.CustomBase):
    title: MockMovies


class MockTrailerService(ITrailerService):
    """Trailer service used to mock the workings of the real service."""

    def __init__(self, config: ConfigBase, cache_provider: ICacheProvider) -> None:
        self._config = config
        self._cache_provider = cache_provider

    @property
    def compact_movie_data_entries(self) -> dict[str, list[models.CompactMovieData]]:
        """Loads the compact movie data lists in memory."""
        compact_movies = {}
        json_files = [
            ('star wars', './tests/data/trailer/search-star-wars2.json'),
            ('lord of the rings', './tests/data/trailer/search-lotr.json'),
            ('indiana jones', './tests/data/trailer/search-indiana-jones.json'),
        ]

        for movie in json_files:
            with open(movie[1], 'r', encoding='utf-8') as f:
                data = json.loads(f.read())
            compact_movies.update(
                {movie[0]: [models.CompactMovieData(**movie_data) for movie_data in data]}
            )

        return compact_movies

    @property
    def movie_data_with_trailer_entries(self) -> dict[str, models.MovieDataWithTrailer]:
        """Loads the movie data with trailers in memory."""
        movie_data_with_trailer = {}
        sources = [
            './tests/data/trailer/trailer-result-starwars.json',
            './tests/data/trailer/trailer-result-lotr.json',
            './tests/data/trailer/trailer-result-indiana-jones.json',
        ]
        for source in sources:
            with open(source, 'r', encoding='utf-8') as f:
                data = json.loads(f.read())

            for movie_with_trailer in data['movies']:
                movie_data_with_trailer.update(
                    {
                        movie_with_trailer['imdbID']: models.MovieDataWithTrailer(
                            **movie_with_trailer
                        )
                    }
                )
        return movie_data_with_trailer

    async def search(self, query: str, network_lag: float = 0) -> TrailerResult:
        """
        Simulates the search for movie data with trailers, the old version..
        the network_lag parameter can be used to simulate network lag.
        """
        await asyncio.sleep(network_lag)

        try:
            compact_movie_list = self.compact_movie_data_entries[query]
        except KeyError:
            raise MovieNotFoundError('MOVIE_NOT_IN_MOCK_DATA')

        movies_with_trailer = [
            self.movie_data_with_trailer_entries[movie.imdbID]
            for movie in compact_movie_list
        ]

        return TrailerResult(movies=movies_with_trailer)

    async def get_movie_data_with_trailer_by_imdb_id(
        self, _id: str, network_lag: float = 0
    ) -> MovieDataWithTrailer:
        """
        Simulates the retreiving of detailed movie information with the trailer.
        the network_lag parameter can be used to simulate network lag.
        """
        await asyncio.sleep(network_lag)
        try:
            movie_data_with_trailer = self.movie_data_with_trailer_entries[_id]
        except KeyError:
            raise InvalidIMDBId('INVALID_IMDB_ID')
        return movie_data_with_trailer

    async def get_compact_movie_data_by_query(
        self, query: str, network_lag: float = 0
    ) -> list[CompactMovieData]:
        """
        Simulates the retreiving of compact movie data with the IMDB id's.
        the network_lag parameter can be used to simulate network lag.
        """
        await asyncio.sleep(network_lag)
        try:
            compact_movie_data = self.compact_movie_data_entries[query.strip()]
        except KeyError:
            raise MovieNotFoundError('MOVIE_NOT_FOUND')
        return compact_movie_data
