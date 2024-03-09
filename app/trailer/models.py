from enum import Enum
from pydantic import Field
from app import models


class MovieData(models.CustomBase):
    Title: str
    Year: str
    Rated: str
    Released: str
    Runtime: str
    Genre: str
    Director: str
    Plot: str
    Poster: str
    imdbRating: str
    imdbID: str


class CompactMovieData(models.CustomBase):
    Title: str
    Year: str
    imdbID: str
    Type: str
    Poster: str


class MovieSearch(models.CustomBase):
    Search: list[CompactMovieData]


class YoutubeTrailerDataSnippet(models.CustomBase):
    publishedAt: str
    channelId: str
    title: str
    description: str
    channelTitle: str


class YoutubeID(models.CustomBase):
    videoId: str


class YoutubeTrailerData(models.CustomBase):
    id: YoutubeID
    snippet: YoutubeTrailerDataSnippet


class MovieDataWithTrailer(MovieData):
    trailer_link: str | None = None


class TrailerResult(models.CustomBase):
    movies: list[MovieDataWithTrailer]
    from_cache: bool = Field(default=False)


class CachePrefixes(str, Enum):
    FULL_RESULT = 'full_result_'
    COMPACT_MOVIE_DATA_LIST = 'compact_movie_data_list_'
    SINGLE_RESULT_BY_ID = 'single_result_by_id_'
