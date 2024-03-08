from abc import ABC, abstractmethod


class IMovieDataProvider(ABC):
    @abstractmethod
    async def search_multi(self, query: str): ...

    @abstractmethod
    async def get_by_id(self, id: str): ...


class ITrailerProvider(ABC):
    @abstractmethod
    async def search_multi_return_first(self, query: str): ...
