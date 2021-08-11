import logging
from typing import Optional

import asyncpg
import numpy as np
import uvicorn
from fastapi import FastAPI
from fastapi.responses import UJSONResponse
from scipy import signal

logging.disable()

query_by_name = '''select student_id, student_name, student_gender, student_birthday 
from test.sc_student where student_name = $1'''

query_all = 'select student_id, student_name, student_gender, student_birthday from test.sc_student'


async def get_connection_pool():
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


async def close_connection_pool():
    global app
    await app.state.connection_pool.close()


app = FastAPI()
app.add_event_handler('startup', get_connection_pool)
app.add_event_handler('shutdown', close_connection_pool)


@app.get('/hello')
async def async_hello(name: Optional[str] = None):
    return {'message': f'Hello {name or "World"}!'}


@app.get('/hello_ujson')
async def async_hello_ujson(name: Optional[str] = None):
    return UJSONResponse({'message': f'Hello {name or "World"}!'})


@app.get('/db')
async def async_db(name: Optional[str] = None):
    pool = app.state.connection_pool
    async with pool.acquire() as conn:
        if name:
            items = await conn.fetch(query_by_name, name)
        else:
            items = await conn.fetch(query_all)
    return [dict(item) for item in items]


@app.get('/numpy')
async def async_numpy():
    arr = np.random.random([1000, 1000])
    core = np.random.random([18, 18])
    conv = signal.convolve2d(arr, core)
    l1 = conv.mean(axis=0).tolist()
    l2 = conv.mean(axis=1).tolist()
    return {'l1': l1, 'l2': l2}


if __name__ == '__main__':
    uvicorn.run(app=app, port=8080)
