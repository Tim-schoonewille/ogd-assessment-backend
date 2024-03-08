from app import models
from app.config import ConfigBase
from app.interfaces import ICacheProvider
from app.trailer.interfaces import IMovieDataProvider, ITrailerProvider
from app.trailer.models import TrailerResult


class TrailerService:
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
        pass

    async def _search_movies_with_trailers(self, query: str) -> models.TrailerResult:
        movies = await self._movie_provider.search_multi(query=query)
        movies_with_trailer = []
        for movie in movies:
            movie_data = await self._movie_provider.get_by_id(_id=movie.imdbID)
            trailer_data = await self._trailer_provider.search_multi_return_first(
                title=movie_data.Title
            )
            movie_data.trailer_id = trailer_data.id.videoId
            movies_with_trailer.append(movie_data)
        return TrailerResult(movies=movies_with_trailer, from_cache=False)
