import uvicorn

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

import logging

logging.disable()


def hello(request: Request):
    name = request.query_params.get('name') or 'World'
    return JSONResponse({'message': f'Hello {name or "World"}!'})


async def async_hello(request: Request):
    name = request.query_params.get('name') or 'World'
    return JSONResponse({'message': f'Hello {name or "World"}!'})


app = Starlette(
    routes=[
        Route('/hello', hello),
        Route('/async/hello', async_hello),
    ]
)

if __name__ == '__main__':
    uvicorn.run(app=app, port=8080)
