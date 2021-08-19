import logging
from json import dumps as json_dumps

import asyncpg
import numpy as np
from sanic import Sanic
from sanic.request import Request
from sanic.response import json
from scipy import signal
from ujson import dumps as ujson_dumps

logging.disable()

query_by_name = '''select student_id, student_name, student_gender, student_birthday 
from test.sc_student where student_name = $1'''

query_all = 'select student_id, student_name, student_gender, student_birthday from test.sc_student'

app = Sanic(name='Sanic')


@app.after_server_start
async def setup_connection_pool(*args, **kwargs):
    app.ctx.connection_pool = await asyncpg.create_pool(
        min_size=16,
        max_size=16,
        user='postgres',
        password='123456',
        database='test',
        host='127.0.0.1',
        port=5432
    )


@app.before_server_stop
async def teardown_connection_pool(*args, **kwargs):
    await app.ctx.connection_pool.close()


@app.get('/hello')
async def async_hello(request: Request):
    name = request.args.get('name', 'World')
    return json({'message': f'Hello {name}!'}, dumps=json_dumps)


@app.get('/hello_ujson')
async def async_hello_ujson(request: Request):
    name = request.args.get('name', 'World')
    return json({'message': f'Hello {name}!'}, dumps=ujson_dumps)


@app.get('/db')
async def async_db(request: Request):
    name = request.args.get('name')
    pool = app.ctx.connection_pool
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
    return json(result)


@app.get('/numpy')
async def async_numpy(_):
    arr = np.random.random([1000, 1000])
    core = np.random.random([18, 18])
    conv = signal.convolve2d(arr, core)
    l1 = conv.mean(axis=0).tolist()
    l2 = conv.mean(axis=1).tolist()
    return json({'l1': l1, 'l2': l2})


if __name__ == '__main__':
    app.run(port=8080)
