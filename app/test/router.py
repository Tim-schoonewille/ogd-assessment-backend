from fastapi import APIRouter


router = APIRouter(prefix='/test', tags=['tests'])


@router.get('/')
def test_route():
    return {'hello': 'world'}
