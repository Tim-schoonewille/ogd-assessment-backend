from json import JSONDecodeError
from fastapi import APIRouter, HTTPException, status

from app import models
from app.trailer.dependencies import GetTrailerService
from app.trailer.exceptions import (
    InvalidIMDBId,
    InvalidTrailerData,
    MovieNotFoundError,
    OmdbApiError,
    YoutubeApiError,
)

router = APIRouter(prefix='/trailer', tags=['trailer-service-v2'])


@router.get(
    path='/search',
    response_model=list[models.CompactMovieData],
    status_code=status.HTTP_200_OK,
    summary='Gets compacted data of movie.',
    description="""
    V2 of the main business logic.

    V1 tends to get slow when the initial movie provider is queried for an overview
    of the possible movies of given title query, thus resulting in a terrible user 
    experience.

    V2 aims to improve UX by seperating the initial request for imdb ID's and getting the 
    data for each individual result of said request.

    Use this endpoint to get a list of movies with iMDB id's. After, 
    use the ID in the other endpoint to get a more detailed response. 

    Seperating these calls gives the user quicker results thus imporving UX.

    Every call is cached to speed up future performance.
    """,
    responses={
        status.HTTP_200_OK: {
            'model': list[models.CompactMovieData],
            'description': 'Returns a list of CompactMovieData models on success.',
        },
        status.HTTP_404_NOT_FOUND: {
            'model': models.HttpError,
            'description': 'Returns a 404 if no result.',
        },
    },
)
async def search_movies_compact_endpoint(title: str, service: GetTrailerService):
    try:
        compact_movie_data_list = await service.get_compact_movie_data_by_query(
            query=title.strip().lower()
        )
    except MovieNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    return compact_movie_data_list


@router.get(
    path='/search/{imdb_id}',
    response_model=models.MovieDataWithTrailer,
    status_code=status.HTTP_200_OK,
    summary='Get movie data with trailer by imdb id.',
    description="""
    Get movie data with trailer by imdb id.
    
    Use this endpoint to get movie data with the trailer after getting imdb ID's from
    the other endpoint.

    The result is cached to speed up future requests.
    """,
    responses={
        status.HTTP_200_OK: {
            'model': models.MovieDataWithTrailer,
            'description': 'Returns a MovieDataWithTrailer object on success.',
        },
        status.HTTP_400_BAD_REQUEST: {
            'model': models.HttpError,
            'description': 'Returns a 400 if there a problem with the youtube api, \
                thee movie data api, or invalid data',
        },
        status.HTTP_404_NOT_FOUND: {
            'model': models.HttpError,
            'description': 'Returns a 404 if the imdb ID is not found.',
        },
    },
)
async def search_movie_data_with_trailer(imdb_id: str, service: GetTrailerService):
    try:
        movie_data_with_trailer = await service.get_movie_data_with_trailer_by_imdb_id(
            _id=imdb_id.lower()
        )
    except InvalidIMDBId as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except OmdbApiError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='OMDB_API_ERROR'
        )
    except YoutubeApiError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='YOUTUBE_API_ERROR'
        )
    except InvalidTrailerData as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='INVALID_IMDB_ID'
        )
    # except ValidationError:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST, detail='INVALID_REQUEST'
    #     )
    return movie_data_with_trailer
