from fastapi import APIRouter, HTTPException, status

from app import models
from app.trailer.dependencies import GetMockTrailerService
from app.trailer.exceptions import InvalidIMDBId, MovieNotFoundError


router = APIRouter(prefix='/trailer', tags=['mock-trailer-v2'])


@router.post('/search')
async def mock_search_movies_compact_endpoint(
    body: models.TrailerSearchForm, service: GetMockTrailerService, network_lag: float = 1
):
    try:
        compact_movie_data = await service.get_compact_movie_data_by_query(
            query=body.title.strip(), network_lag=network_lag
        )
    except MovieNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return compact_movie_data


@router.post('/search/{imdb_id}', response_model=models.MovieDataWithTrailer)
async def mock_search_movie_with_trailer_data_endpoint(
    imdb_id: str,
    body: models.TrailerSearchForm,
    service: GetMockTrailerService,
    network_lag: float = 1,
):
    try:
        movie_with_trailer_data = await service.get_movie_data_with_trailer_by_imdb_id(
            _id=imdb_id, title=body.title.strip(), network_lag=network_lag
        )
    except InvalidIMDBId as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return movie_with_trailer_data
