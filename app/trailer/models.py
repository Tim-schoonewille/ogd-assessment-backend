from enum import Enum

from pydantic import Field

from app import models


class MovieData(models.CustomBase):
    """Pydantic class that models the response from the OMDB API."""

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
    """Pydantic class that models esponse from the search endpoint of the OMDB API."""

    Title: str
    Year: str
    imdbID: str
    Type: str
    Poster: str


class MovieSearch(models.CustomBase):
    Search: list[CompactMovieData]


class YoutubeTrailerDataSnippet(models.CustomBase):
    """Snippet part from youtube api search response."""

    publishedAt: str
    channelId: str
    title: str
    description: str
    channelTitle: str


class YoutubeID(models.CustomBase):
    """Video ID part from the youtube api search response."""

    videoId: str


class YoutubeTrailerData(models.CustomBase):
    """Pydantic class that models the response from the youtube data api."""

    id: YoutubeID
    snippet: YoutubeTrailerDataSnippet


class MovieDataWithTrailer(MovieData):
    """
    Inherits all it's attributes from MovieData
    with the link of the trailer appended to it
    """

    trailer_link: str | None = None
    trailer_embed_link: str | None = None


class TrailerResult(models.CustomBase):
    """Models the full result that returns from V1 Trailer Service."""

    movies: list[MovieDataWithTrailer]
    from_cache: bool = Field(default=False)


class CachePrefixes(str, Enum):
    """Enum for reusable cache prefixes."""

    FULL_RESULT = 'full_result_'
    COMPACT_MOVIE_DATA_LIST = 'compact_movie_data_list_'
    SINGLE_RESULT_BY_ID = 'single_result_by_id_'


class TrailerSearchForm(models.CustomBase):
    """Search form for fastaAPI endpoints used in the Request body."""

    title: str
