from abc import ABC, abstractmethod
from typing import Any


class ICacheProvider(ABC):
    """Interface for cache providers."""

    @abstractmethod
    async def get_str(self, key: str) -> str: ...

    @abstractmethod
    async def get_json(self, key: str) -> dict[str, Any] | list[dict[str, Any]]: ...

    @abstractmethod
    async def store_str(self, key: str, value: str) -> None: ...

    @abstractmethod
    async def store_json(
        self, key: str, value: dict[str, Any] | list[dict[str, Any]]
    ) -> None: ...
