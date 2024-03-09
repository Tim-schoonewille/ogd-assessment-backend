from app import models
from app.config import ConfigBase
from app.interfaces import ICacheProvider
from app.trailer.interfaces import IMovieDataProvider, ITrailerProvider, ITrailerService
from app.trailer.models import (
    CompactMovieData,
    MovieDataWithTrailer,
    TrailerResult,
    YoutubeTrailerData,
)


# class MockMovieDataProvider(IMovieDataProvider):
#     async def search_multi(self, query: str) -> list[CompactMovieData]:
#         return None

#     async def get_by_id(self, _id: str) -> MovieDataWithTrailer:
#         return None


# class MockTrailerProvider(ITrailerProvider):
#     async def search_multi_return_first(self, title: str) -> YoutubeTrailerData:
#         return None


class MockTrailerService(ITrailerService):
    def __init__(self, config: ConfigBase, cache_provider: ICacheProvider) -> None:
        self._config = config
        self._cache_provider = cache_provider

    @property
    def compact_movie_data_entries(self) -> dict[str, list[models.CompactMovieData]]:
        pass

    @property
    def movie_data_with_trailer_entries(self) -> dict[str, models.MovieDataWithTrailer]:
        pass

    async def search(self, query: str) -> TrailerResult:
        return None

    async def get_movie_data_with_trailer_by_imdb_id(
        self, _id: str, title: str
    ) -> MovieDataWithTrailer:
        return None

    async def get_compact_movie_data_by_query(self, query: str) -> list[CompactMovieData]:
        return None
