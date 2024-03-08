from abc import ABC, abstractmethod

from app import models


class IMovieDataProvider(ABC):
    @abstractmethod
    async def search_multi(self, query: str) -> list[models.CompactMovieData]: ...

    @abstractmethod
    async def get_by_id(self, _id: str) -> models.MovieDataWithTrailer: ...


class ITrailerProvider(ABC):
    @abstractmethod
    async def search_multi_return_first(
        self, title: str
    ) -> models.YoutubeTrailerData: ...
