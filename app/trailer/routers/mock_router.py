from fastapi import APIRouter, HTTPException, status

from app import models
from app.trailer.dependencies import GetMockTrailerService
from app.trailer.exceptions import MovieNotFoundError


router = APIRouter(prefix='/trailer', tags=['mock-trailer-v1'])


@router.post(
    path='/search',
    response_model=models.TrailerResult,
    status_code=status.HTTP_200_OK,
    summary='Search for a trailer with meta data.',
    deprecated=True,
    description="""
    The mock version of getting a trailer with meta data based on the given query (title).

    All data resides in application memory and is not fetched from an external api or 
    cache.

    Currently only has three different query titles:
    - 'star wars'
    - 'lord of the rings'
    - 'indiana jones'

    It has a query parameter 'network_lag: float' to simulate a long network request,
    since the original version of this can take a long time to process. 
    It defaults to 10.0 seconds, but can be overwritten using the query parameter.
    """,
    responses={
        status.HTTP_200_OK: {
            'model': models.TrailerResult,
            'description': 'The return model of a successfull query.',
        },
        status.HTTP_404_NOT_FOUND: {
            'model': models.HttpError,
            'description': 'Returns a 404 if the queried movie is not in app memory',
        },
    },
)
async def search_trailers(
    *,
    network_lag: float = 10,
    body: models.TrailerSearchForm,
    service: GetMockTrailerService,
):
    try:
        trailer_result = await service.search(query=body.title, network_lag=network_lag)
    except MovieNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return trailer_result
