from hashlib import md5
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from fastapi import Request, Response
from fastapi.concurrency import iterate_in_threadpool


class CacheHeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        response = await call_next(request)

        response_body = [chunk async for chunk in response.body_iterator]  # type: ignore
        response.body_iterator = iterate_in_threadpool(iter(response_body))  # type: ignore
        body = response_body[0]

        if 'If-None-Match' in request.headers:
            print('It is in the headers!!!!')
            current_etag = md5(body).hexdigest()
            client_etag = request.headers['If-None-Match']

            if current_etag == client_etag:
                print('Etags match!')
                response.status_code = 304
                return response
        response.headers.update({'Cache-Control': 'public, max-age=10'})
        etag = md5(body).hexdigest()

        response.headers.update({'ETag': str(etag)})

        return response
