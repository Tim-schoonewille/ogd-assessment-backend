from fastapi import APIRouter, HTTPException, status

from app import models
from app.redis import GetAsyncCache
from app.trailer.dependencies import GetMockTrailerService
from app.trailer.exceptions import MovieNotFoundError


router = APIRouter(prefix='/trailer', tags=['mock-trailer-v1'])


@router.post('/search', response_model=models.TrailerResult)
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
