from fastapi import APIRouter, HTTPException, status

from app import models
from app.trailer.dependencies import GetTrailerService
from app.trailer.exceptions import MovieNotFoundError


router = APIRouter(prefix='/trailer', tags=['trailer-service-v1'])


@router.post('/search', response_model=models.TrailerResult)
async def search_trailers_v1(body: models.TrailerSearchForm, service: GetTrailerService):
    try:
        trailer_result = await service.search(query=body.title.strip())
    except MovieNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return trailer_result
