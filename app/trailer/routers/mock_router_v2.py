from fastapi import APIRouter, HTTPException, status

from app import models
from app.trailer.dependencies import GetMockTrailerService
from app.trailer.exceptions import InvalidIMDBId, MovieNotFoundError
from tests.data.trailer.mock_utilities import MockMovies


router = APIRouter(prefix='/trailer', tags=['mock-trailer-v2'])


@router.post(
    path='/search',
    response_model=list[models.CompactMovieData],
    status_code=status.HTTP_200_OK,
    summary='Get compacted data of movie from application memory',
    description="""
    The mock version of the v2 approach.

    Use this to test your frontend code.

    Has a query parameter (network_lag: float) that allows you to simulate a
    network request. This defaults to 1 second.

    Currently, only three movies are in application memory:

    - 'star wars'
    - 'lord of the rings'
    - 'indiana jones'
    """,
    responses={
        status.HTTP_200_OK: {
            'model': list[models.CompactMovieData],
            'description': 'Returns a list of CompactMovieData objects on success.',
        },
        status.HTTP_404_NOT_FOUND: {
            'model': models.HttpError,
            'description': 'Returns a 404 if a movie was given that is not in memory.',
        },
    },
)
async def mock_search_movies_compact_endpoint(
    title: MockMovies,
    service: GetMockTrailerService,
    network_lag: float = 1,
):
    try:
        compact_movie_data = await service.get_compact_movie_data_by_query(
            query=title, network_lag=network_lag
        )
    except MovieNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return compact_movie_data


@router.post(
    path='/search/{imdb_id}',
    response_model=models.MovieDataWithTrailer,
    status_code=status.HTTP_200_OK,
    summary='Get movie data with trailer by imdb.id',
    description="""
    Mock version of similair v2 endpoint.

    For every result gotten in the other endpoint, there is MovieDataWithTrailer in JSON
    representation in memory. You can receive this by inserting the iMDB id.

    Simulate network latency by using query parameter: network_lag: float (defaults to 1)

    json body containing title will be deprecated soon
    """,
    responses={
        status.HTTP_200_OK: {
            'model': models.MovieDataWithTrailer,
            'description': 'Returns a MovieDataWithTrailer object on success.',
        },
        status.HTTP_404_NOT_FOUND: {
            'model': models.HttpError,
            'description': 'Returns a 404 if the imdb id is not in application memory.',
        },
    },
)
async def mock_search_movie_with_trailer_data_endpoint(
    imdb_id: str,
    body: models.TrailerSearchForm,
    service: GetMockTrailerService,
    network_lag: float = 1,
):
    try:
        movie_with_trailer_data = await service.get_movie_data_with_trailer_by_imdb_id(
            _id=imdb_id, title=body.title, network_lag=network_lag
        )
    except InvalidIMDBId as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return movie_with_trailer_data
