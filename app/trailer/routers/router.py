from fastapi import APIRouter, HTTPException, status

from app import models
from app.trailer.dependencies import GetTrailerService
from app.trailer.exceptions import MovieNotFoundError

router = APIRouter(prefix='/trailer', tags=['trailer-service-v1'])


@router.post(
    path='/search',
    response_model=models.TrailerResult,
    status_code=status.HTTP_200_OK,
    description="""
    V1 of getting a trailer with meta data based on the given query(title).

    If there are a lot of movies in the initial result, this will take quite a while
    to load the rest of the data (meta-data/trailer).

    Therefore, it is recommended to use
    the V2 version. 
    """,
    deprecated=True,
    summary='Search for a trailer with meta data.',
    responses={
        status.HTTP_200_OK: {
            'model': models.TrailerResult,
            'description': 'The return model of a successfull query.',
        },
        status.HTTP_404_NOT_FOUND: {
            'model': models.HttpError,
            'description': 'Returns a 404 if the movie is not found.',
        },
    },
)
async def search_trailers_v1(body: models.TrailerSearchForm, service: GetTrailerService):
    try:
        trailer_result = await service.search(query=body.title.strip())
    except MovieNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    return trailer_result
