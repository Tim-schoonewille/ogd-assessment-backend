from fastapi import APIRouter, HTTPException, status
from pydantic import ValidationError

from app import models
from app.trailer.dependencies import GetTrailerService
from app.trailer.exceptions import InvalidIMDBId, MovieNotFoundError


router = APIRouter(prefix='/trailer', tags=['trailer-service-v2'])


@router.post('/search', response_model=list[models.CompactMovieData])
async def search_movies_compact_endpoint(
    body: models.TrailerSearchForm, service: GetTrailerService
):
    try:
        compact_movie_data_list = await service.get_compact_movie_data_by_query(
            query=body.title.strip()
        )
    except MovieNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return compact_movie_data_list


@router.post('/search/{imdb_id}', response_model=models.MovieDataWithTrailer)
async def search_movie_data_with_trailer(
    imdb_id: str, body: models.TrailerSearchForm, service: GetTrailerService
):
    try:
        movie_data_with_trailer = await service.get_movie_data_with_trailer_by_imdb_id(
            _id=imdb_id, title=body.title.strip()
        )
    except InvalidIMDBId as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValidationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='INVALID_REQUEST'
        )
    return movie_data_with_trailer
