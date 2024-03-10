from abc import ABC, abstractmethod

from app import models


class IMovieDataProvider(ABC):
    """Interface for movie provider classes."""

    @abstractmethod
    async def search_multi(self, query: str) -> list[models.CompactMovieData]: ...

    @abstractmethod
    async def get_by_id(self, _id: str) -> models.MovieDataWithTrailer: ...


class ITrailerProvider(ABC):
    """Interface for trailer provider classes."""

    @abstractmethod
    async def search_multi_return_first(
        self, title: str
    ) -> models.YoutubeTrailerData: ...


class ITrailerService(ABC):
    """Interface for trailer service classes."""

    @abstractmethod
    async def search(self, query: str) -> models.TrailerResult: ...

    @abstractmethod
    async def get_movie_data_with_trailer_by_imdb_id(
        self, _id: str, title: str
    ) -> models.MovieDataWithTrailer: ...

    @abstractmethod
    async def get_compact_movie_data_by_query(
        self, query: str
    ) -> list[models.CompactMovieData]: ...
