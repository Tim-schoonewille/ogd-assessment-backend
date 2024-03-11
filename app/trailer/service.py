from typing import Any
from app import models
from app.config import ConfigBase
from app.interfaces import ICacheProvider
from app.trailer.interfaces import IMovieDataProvider, ITrailerProvider, ITrailerService
from app.trailer.models import TrailerResult


class TrailerService(ITrailerService):
    """
    Class with all the business logic for the trailer service.

    Dependencies:
        config (ConfigBase):
            Global configuration object.

        movie_provider (IMovieProvider):
            Any movie provider that adheres to the interface

        trailer_provider (ITrailerProvider):
            Any trailer provider that adheres to the interface

        cache_provider (ICacheProvider):
            Any cache provider that adheres to the interface.

    v1-methods:
        .search()

    v2-methods:
        .get_movie_data_with_trailer_by_imdb_id()

        .get_compact_movie_data_by_query()
    """

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
        """
        Search for movie trailers and return them all in one big result.

        Every result is cached, therefore it will try to fetch the data from the cache.
        If it is not present, it will initiate a new search, using the private search
        movie with trailers method.

        Due to having to perform many requests in one function, this tends to be slow if
        the query gets a multitude of movies from the initial query.

        Recommended using the V2 approach.

        Args:
            query (str):
                Intended for the title of the movie(s) of which to query data for.

        Returns:
            TrailerResult:
                Pydantic model that houses a list of MovieDataWithTrailer objects.
                Also has a 'from_cache' flag.
        """
        result_from_cache = await self._cache_provider.get_json(
            key=f'{models.CachePrefixes.FULL_RESULT}{query}'
        )
        if result_from_cache is not None:
            result_from_cache = models.TrailerResult(**result_from_cache)  # type: ignore
            result_from_cache.from_cache = True
            return result_from_cache
        movies_with_trailers = await self._search_movies_with_trailers(query=query)
        await self._cache_provider.store_json(
            key=f'{models.CachePrefixes.FULL_RESULT}{query}',
            value=movies_with_trailers.model_dump(),
        )
        return movies_with_trailers

    async def _search_movies_with_trailers(self, query: str) -> models.TrailerResult:
        """
        The logic behind getting all the data for TrailerResult.

        Utelizing the movie provider's search multi method, it gets a compact list
        of all the movies associated with the users' query.
        It then retreives more data for every entry of the list and queries an external
        api via the trailer provider for the trailer link.
        It constructs a working link for every movie.

        This can take quite long if the initial result from search multi is extensive.
        Therefore it is recommended to use the V2 approach.

        Args:
            query (str):
                Intended for the title of the movie(s) of which to query data for.

        Returns:
            TrailerResult:
                Pydantic model that houses a list of MovieDataWithTrailer objects.
        """
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
            movie_data.trailer_embed_link = (
                f'https://wwww.youtube.com/embed/{trailer_data.id.videoId}'
            )
            movies_with_trailer.append(movie_data)
        return TrailerResult(movies=movies_with_trailer, from_cache=False)

    async def get_movie_data_with_trailer_by_imdb_id(
        self, _id: str, title: str
    ) -> models.MovieDataWithTrailer:
        """
        Use a iMDB identifier to query the movie provider for movie data.

        After receiving the data, it aggregates the result in one single
        object: MovieDataWithTrailer

        Before querying an external API, it will check the cache register if the data
        is already present, if not, it will store the result in cache afterwards, using
        the appropriate prefix and appending the iMDB id to it.

        This is part of the V2 approach.

        Args:
            _id (str):
                A iMDB identifier for the movie.

            title (str):
                The title of the movie. THIS WILL BE DEPRECATED SOON. The initial response
                of the movie provider will have the title, so it's of no use to pass it
                as an argument.

        Returns:
            MovieDataWithTrailer:
                Pydantic model with meta-data about the movie and a useable trailer link.
        """
        # TODO Remove the title argument.
        cache_key = f'{models.CachePrefixes.SINGLE_RESULT_BY_ID}{_id}'
        movie_data_with_trailer_in_cache = await self._cache_provider.get_json(cache_key)

        if self._validate_cached_movie_data_with_trailer(
            movie_data_with_trailer_in_cache  # type: ignore
        ):
            return models.MovieDataWithTrailer(**movie_data_with_trailer_in_cache)  # type: ignore

        movie_data = await self._movie_provider.get_by_id(_id=_id)
        trailer_data = await self._trailer_provider.search_multi_return_first(
            title=movie_data.Title
        )
        movie_data.trailer_link = (
            f'https://www.youtube.com/watch?v={trailer_data.id.videoId}'
        )
        movie_data.trailer_embed_link = (
            f'https://www.youtube.com/embed/{trailer_data.id.videoId}'
        )

        await self._cache_provider.store_json(
            key=cache_key, value=movie_data.model_dump()
        )
        return movie_data

    async def get_compact_movie_data_by_query(
        self, query: str
    ) -> list[models.CompactMovieData]:
        """
        Responsible for getting a list of movies from the movie provider.
        Each entry in the list holds an iMDB id for further querying.

        It will first check the cache registry if the data is already present,
        if not, resumes to query the external API using the movie provider and
        storing the result in the cache using the appropriate prefix, suffixing
        the query to it for future usecases.

        This is part of the V2 approach.

        Args:
            query (str):
                Intended for the title of the movie(s) of which to query data for.

        Returns:
            list[CompactMovieData]:
                A list that contains the pydantic model for every movie found
                via the movie provider.
        """
        cache_key = f'{models.CachePrefixes.COMPACT_MOVIE_DATA_LIST}{query}'
        compact_movie_data_in_cache = await self._cache_provider.get_json(cache_key)

        if self._validate_cached_compact_movie_data(compact_movie_data_in_cache):  # type: ignore
            compact_movie_data_list = [
                models.CompactMovieData(**movie_data)
                for movie_data in compact_movie_data_in_cache
                if isinstance(movie_data, dict)
            ]
            return compact_movie_data_list

        compact_movie_data_list = await self._movie_provider.search_multi(query=query)
        await self._cache_provider.store_json(
            key=cache_key,
            value=[movie_data.model_dump() for movie_data in compact_movie_data_list],
        )
        return compact_movie_data_list

    def _validate_cached_compact_movie_data(
        self, list_compact_movie_data: list[dict[str, Any]] | None
    ) -> bool:
        if list_compact_movie_data is None:
            return False
        for compact_movie_data in list_compact_movie_data:
            keys_in_compact_movie_data = compact_movie_data.keys()
            keys_in_model = models.CompactMovieData.__annotations__.keys()
            if keys_in_compact_movie_data != keys_in_model:
                return False
        return True

    def _validate_cached_movie_data_with_trailer(
        self, movie_data_with_trailer: dict[str, Any] | None
    ) -> bool:
        if movie_data_with_trailer is None:
            return False
        keys_in_movie_data_with_trailer = list(movie_data_with_trailer.keys())
        keys_in_model = list(models.MovieData.__annotations__.keys()) + list(
            models.MovieDataWithTrailer.__annotations__.keys()
        )
        print(keys_in_movie_data_with_trailer)
        print(keys_in_model)
        return keys_in_movie_data_with_trailer == keys_in_model
