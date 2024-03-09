from app import models
from app.config import ConfigBase
from app.interfaces import ICacheProvider
from app.trailer.interfaces import IMovieDataProvider, ITrailerProvider, ITrailerService
from app.trailer.models import TrailerResult


class TrailerService(ITrailerService):
    def __init__(
        self,
        config: ConfigBase,
        movie_provider: IMovieDataProvider,
        trailer_provider: ITrailerProvider,
        cache_provider: ICacheProvider,
    ) -> None:
        self._config = config
        self._movie_provider = movie_provider
        self._trailer_provider = trailer_provider
        self._cache_provider = cache_provider

    async def search(self, query: str) -> models.TrailerResult:
        result_from_cache = await self._cache_provider.get_json(
            key=f'{models.CachePrefixes.FULL_RESULT}{query}'
        )
        if result_from_cache is not None:
            result_from_cache = models.TrailerResult(**result_from_cache)
            result_from_cache.from_cache = True
            return result_from_cache
        movies_with_trailers = await self._search_movies_with_trailers(query=query)
        await self._cache_provider.store_json(
            key=f'{models.CachePrefixes.FULL_RESULT}{query}',
            value=movies_with_trailers.model_dump(),
        )
        return movies_with_trailers

    async def _search_movies_with_trailers(self, query: str) -> models.TrailerResult:
        movies = await self._movie_provider.search_multi(query=query)
        movies_with_trailer = []
        for movie in movies:
            movie_data = await self._movie_provider.get_by_id(_id=movie.imdbID)
            trailer_data = await self._trailer_provider.search_multi_return_first(
                title=movie_data.Title
            )
            movie_data.trailer_link = (
                f'https://www.youtube.com/watch?v={trailer_data.id.videoId}'
            )
            movies_with_trailer.append(movie_data)
        return TrailerResult(movies=movies_with_trailer, from_cache=False)

    async def get_movie_data_with_trailer_by_imdb_id(
        self, _id: str, title: str
    ) -> models.MovieDataWithTrailer:
        cache_key = f'{models.CachePrefixes.SINGLE_RESULT_BY_ID}{_id}'
        movie_data_with_trailer_in_cache = await self._cache_provider.get_json(cache_key)

        if movie_data_with_trailer_in_cache:
            return models.MovieDataWithTrailer(**movie_data_with_trailer_in_cache)

        movie_data = await self._movie_provider.get_by_id(_id=_id)
        trailer_data = await self._trailer_provider.search_multi_return_first(
            title=movie_data.Title
        )
        movie_data.trailer_link = (
            f'https://www.youtube.com/watch?v={trailer_data.id.videoId}'
        )

        await self._cache_provider.store_json(
            key=cache_key, value=movie_data.model_dump()
        )
        return movie_data

    async def get_compact_movie_data_by_query(
        self, query: str
    ) -> list[models.CompactMovieData]:
        cache_key = f'{models.CachePrefixes.COMPACT_MOVIE_DATA_LIST}{query}'
        compact_movie_data_in_cache = await self._cache_provider.get_json(cache_key)

        if compact_movie_data_in_cache:
            compact_movie_data_list = [
                models.CompactMovieData(**movie_data)
                for movie_data in compact_movie_data_in_cache.values()
            ]
            return compact_movie_data_list

        compact_movie_data_list = await self._movie_provider.search_multi(query=query)
        await self._cache_provider.store_json(
            key=cache_key,
            value=[movie_data.model_dump() for movie_data in compact_movie_data_list],
        )
        return compact_movie_data_list
