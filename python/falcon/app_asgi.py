import logging
from datetime import datetime
from json import dumps as json_dumps
from typing import Optional

import asyncpg
import falcon.asgi
import numpy as np
import uvicorn
from falcon.request import Request
from falcon.response import Response
from scipy import signal
from ujson import dumps as ujson_dumps

logging.disable()

query_by_name = '''select student_id, student_name, student_gender, student_birthday 
from test.sc_student where student_name = $1'''

query_all = 'select student_id, student_name, student_gender, student_birthday from test.sc_student'

async_connection_pool: Optional[asyncpg.pool.Pool] = None


class DatabaseMiddleware:

    async def process_startup(self, scope, event):
        global async_connection_pool
        async_connection_pool = await asyncpg.create_pool(
            min_size=16,
            max_size=16,
            user='postgres',
            password='123456',
            database='test',
            host='127.0.0.1',
            port=5432
        )

    async def process_shutdown(self, scope, event):
        global async_connection_pool
        await async_connection_pool.close()


class HelloResource:

    async def on_get(self, req: Request, resp: Response):
        name = req.params.get('name', 'World')
        resp.text = json_dumps({'message': f'Hello {name}!'})


class HelloUJsonResource:

    async def on_get(self, req: Request, resp: Response):
        name = req.params.get('name', 'World')
        resp.text = ujson_dumps({'message': f'Hello {name}!'})


class DatabaseResource:

    async def on_get(self, req: Request, resp: Response):
        name = req.params.get('name')
        global async_connection_pool
        async with async_connection_pool.acquire() as conn:
            if name:
                items = await conn.fetch(query_by_name, name)
            else:
                items = await conn.fetch(query_all)
        result = [dict(item) for item in items]
        for r in result:
            dt: datetime = r['student_birthday']
            r['student_birthday'] = dt.strftime('%Y-%m-%d')
        resp.text = json_dumps(result)


class NumpyResource:

    async def on_get(self, _: Request, resp: Response):
        arr = np.random.random([1000, 1000])
        core = np.random.random([18, 18])
        conv = signal.convolve2d(arr, core)
        l1 = conv.mean(axis=0).tolist()
        l2 = conv.mean(axis=1).tolist()
        resp.text = json_dumps({'l1': l1, 'l2': l2})


app = falcon.asgi.App()

app.add_middleware(DatabaseMiddleware())

app.add_route('/hello', HelloResource())
app.add_route('/hello_ujson', HelloUJsonResource())
app.add_route('/db', DatabaseResource())
app.add_route('/numpy', NumpyResource())

if __name__ == '__main__':
    uvicorn.run(app=app, port=8080)
