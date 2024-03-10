from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class CustomBase(BaseModel):
    """Custom pydantic basemodel. Converts it's output to camel case."""

    model_config = ConfigDict(
        alias_generator=to_camel, populate_by_name=True, from_attributes=True
    )


class EndpointResponse(CustomBase):
    """Model for generic responses using the 'detail' key."""

    detail: str


class HttpError(CustomBase):
    """Model when a HTTP Exception occurs."""

    detail: str


from app.trailer.models import (  # noqa
    MovieData,
    CompactMovieData,
    YoutubeID,
    YoutubeTrailerData,
    YoutubeTrailerDataSnippet,
    MovieDataWithTrailer,
    TrailerResult,
    CachePrefixes,
    TrailerSearchForm,
)

MovieDataWithTrailer.model_rebuild()
