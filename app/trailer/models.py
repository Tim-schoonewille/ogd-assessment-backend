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
