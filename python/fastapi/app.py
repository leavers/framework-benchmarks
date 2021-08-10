from typing import Optional

import os
import asyncpg
import numpy as np
import uvicorn
from fastapi import FastAPI
from fastapi.responses import UJSONResponse
from psycopg2.pool import ThreadedConnectionPool
from scipy import signal

# import logging
#
# logging.disable()


query_by_name = '''select student_id, student_name, student_gender, student_birthday 
from test.sc_student where student_name = %s'''

async_query_by_name = '''select student_id, student_name, student_gender, student_birthday 
from test.sc_student where student_name = $1'''

query_all = 'select student_id, student_name, student_gender, student_birthday from test.sc_student'


def connection_pool():
    global _connection_pool
    if not _connection_pool:
        _connection_pool = ThreadedConnectionPool(
            minconn=os.cpu_count(),
            maxconn=128,
            database='test',
            user='postgres',
            password='123456',
            host='127.0.0.1',
            port=5432,
        )
    return _connection_pool


async def async_connection_pool():
    global _async_connection_pool
    if not _async_connection_pool:
        _async_connection_pool = await asyncpg.create_pool(
            user='postgres',
            password='123456',
            database='test',
            host='127.0.0.1',
            port=5432
        )
    return _async_connection_pool


_connection_pool = None
_async_connection_pool = None

app = FastAPI()


@app.get('/hello')
def hello(name: Optional[str] = None):
    return {'message': f'Hello {name or "World"}!'}


@app.get('/async/hello')
async def async_hello(name: Optional[str] = None):
    return {'message': f'Hello {name or "World"}!'}


@app.get('/hello_ujson')
def hello_ujson(name: Optional[str] = None):
    return UJSONResponse({'message': f'Hello {name or "World"}!'})


@app.get('/async/hello_ujson')
async def async_hello_ujson(name: Optional[str] = None):
    return UJSONResponse({'message': f'Hello {name or "World"}!'})


@app.get('/db')
def db(name: Optional[str] = None):
    pool = connection_pool()
    conn = pool.getconn()
    cur = conn.cursor()
    if name:
        cur.execute(query_by_name, (name,))
    else:
        cur.execute(query_all)
    items = cur.fetchall()
    result = []
    for item in items:
        result.append({
            'student_id': item[0],
            'student_name': item[1],
            'student_gender': item[2],
            'student_birthday': item[3],
        })
    return result


@app.get('/async/db')
async def async_db(name: Optional[str] = None):
    async with (await async_connection_pool()).acquire() as conn:
        if name:
            items = await conn.fetch(async_query_by_name, name)
        else:
            items = await conn.fetch(query_all)
    return [dict(item) for item in items]


@app.get('/async/numpy')
def numpy():
    arr = np.random.random([1000, 1000])
    core = np.random.random([18, 18])
    conv = signal.convolve2d(arr, core)
    l1 = conv.mean(axis=0).tolist()
    l2 = conv.mean(axis=1).tolist()
    return {'l1': l1, 'l2': l2}


@app.get('/async/numpy')
async def async_numpy():
    arr = np.random.random([1000, 1000])
    core = np.random.random([18, 18])
    conv = signal.convolve2d(arr, core)
    l1 = conv.mean(axis=0).tolist()
    l2 = conv.mean(axis=1).tolist()
    return {'l1': l1, 'l2': l2}


if __name__ == '__main__':
    uvicorn.run(app=app, port=8080)
