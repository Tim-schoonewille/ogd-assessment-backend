import json
from app import models
from app.trailer.service import TrailerService

STARWARS_SEARCH_JSON_FILEPATH = './tests/data/trailer/search-star-wars.json'


# async def test_trailer_service(trailer_service: TrailerService) -> None:
#     QUERY = 'star wars'
#     with open(STARWARS_SEARCH_JSON_FILEPATH, 'r', encoding='utf-8') as f:
#         data = json.loads(f.read())['Search']

#     result = await trailer_service._search_movies_with_trailers(query=QUERY)

#     assert isinstance(result, models.TrailerResult)
#     assert result.from_cache is False

#     for movie in result.movies:
#         print('movie title: ', movie.Title)
#         link = f'https://www.youtube.com/watch?v={movie.trailer_id}'
#         print('youtube link:', link)

#     for i, value in enumerate(data):
#         assert value['Title'] == result.movies[i].Title


async def test_trailer_service_pulp_fiction(trailer_service: TrailerService) -> None:
    result = await trailer_service._search_movies_with_trailers(query='pulp fiction')

    for movie in result.movies:
        print('movie title: ', movie.Title)
        link = f'https://www.youtube.com/watch?v={movie.trailer_id}'
        print('youtube link:', link)

    assert 1 == 0
