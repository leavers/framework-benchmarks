import logging

import numpy as np
import uvicorn
import asyncpg
from scipy import signal
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from starlette.routing import Route
from ujson import dumps as ujson_dumps

# logging.disable()

query_by_name = '''select student_id, student_name, student_gender, student_birthday 
from test.sc_student where student_name = $1'''

query_all = 'select student_id, student_name, student_gender, student_birthday from test.sc_student'


class UJSONResponse(Response):
    media_type = "application/json"

    def render(self, content) -> bytes:
        return ujson_dumps(content).encode("utf-8")


async def setup_connection_pool():
    global app
    app.state.connection_pool = await asyncpg.create_pool(
        min_size=16,
        max_size=16,
        user='postgres',
        password='123456',
        database='test',
        host='127.0.0.1',
        port=5432
    )


async def teardown_connection_pool():
    global app
    await app.state.connection_pool.close()


async def async_hello(request: Request):
    name = request.query_params.get('name', 'World')
    return JSONResponse({'message': f'Hello {name}!'})


async def async_hello_ujson(request: Request):
    name = request.query_params.get('name', 'World')
    return UJSONResponse({'message': f'Hello {name}!'})


async def async_db(request: Request):
    name = request.query_params.get('name')
    pool = app.state.connection_pool
    async with pool.acquire() as conn:
        if name:
            items = await conn.fetch(query_by_name, name)
        else:
            items = await conn.fetch(query_all)
    result = []
    for item in items:
        result.append({
            'student_id': item[0],
            'student_name': item[1],
            'student_gender': item[2],
            'student_birthday': item[3].strftime('%Y-%m-%d'),
        })
    return JSONResponse(result)


async def async_numpy(_):
    arr = np.random.random([1000, 1000])
    core = np.random.random([18, 18])
    conv = signal.convolve2d(arr, core)
    l1 = conv.mean(axis=0).tolist()
    l2 = conv.mean(axis=1).tolist()
    return JSONResponse({'l1': l1, 'l2': l2})


app = Starlette(
    routes=[
        Route('/hello', async_hello),
        Route('/hello_ujson', async_hello_ujson),
        Route('/db', async_db),
        Route('/numpy', async_numpy),
    ],
    on_startup=[setup_connection_pool],
    on_shutdown=[teardown_connection_pool],
)

if __name__ == '__main__':
    uvicorn.run(app=app, port=8080)
