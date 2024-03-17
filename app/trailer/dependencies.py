from typing import Annotated, TypeAlias

from fastapi import Depends

from app.config import GetConfig
from app.redis import GetAsyncCache
from app.trailer.interfaces import ITrailerService
from app.trailer.service import TrailerService
from app.trailer.utils import OMDBMovieDataProvider, YoutubeTrailerProvider
from app.utilities import CacheProvider
from tests.data.trailer.mock_utilities import MockTrailerService


async def get_trailer_service(config: GetConfig, cache: GetAsyncCache) -> ITrailerService:
    """
    Dependency for FastAPI endpoints.
    Creates the TrailerService object with dependencies inserted.

    It's dependencies are: MovieProvider, TrailerProvider, CacheProvider, ConfigBase

    Args:
        config (ConfigBase): Configuration object.
        cache (AsyncRedis): The Asynchronous redis client.

    Returns:
        TrailerService: A Fully instantiated TrailserService object.
    """
    movie_provider = OMDBMovieDataProvider(config=config)

    trailer_provider = YoutubeTrailerProvider(config=config)

    cache_provider = CacheProvider(
        cache_client=cache, cache_expire=config.CACHE_EXPIRATION
    )

    service = TrailerService(
        config=config,
        movie_provider=movie_provider,
        trailer_provider=trailer_provider,
        cache_provider=cache_provider,
    )

    return service


async def get_mock_trailer_service(
    config: GetConfig, cache: GetAsyncCache
) -> MockTrailerService:
    """
    Returns a mock version of the TrailerService object for FastAPI endpoints.

    Args:
        config (ConfigBase): Configuration object.
        cache (AsyncRedis): The Asynchronous redis client.

    Returns:
        TrailerService: A Fully instantiated TrailserService object.
    """
    cache_provider = CacheProvider(
        cache_client=cache, cache_expire=config.CACHE_EXPIRATION
    )
    
    service = MockTrailerService(
        config=config,
        cache_provider=cache_provider,
    )

    return service


GetTrailerService: TypeAlias = Annotated[TrailerService, Depends(get_trailer_service)]
GetMockTrailerService: TypeAlias = Annotated[
    MockTrailerService, Depends(get_mock_trailer_service)
]
