import logging
from typing import Optional

import numpy as np
import uvicorn
from fastapi import FastAPI
from fastapi.responses import UJSONResponse
from psycopg2.pool import ThreadedConnectionPool
from scipy import signal

logging.disable()

query_by_name = '''select student_id, student_name, student_gender, student_birthday 
from test.sc_student where student_name = %s'''

query_all = 'select student_id, student_name, student_gender, student_birthday from test.sc_student'


def get_connection_pool():
    global app
    app.state.connection_pool = ThreadedConnectionPool(
        minconn=16,
        maxconn=16,
        database='test',
        user='postgres',
        password='123456',
        host='127.0.0.1',
        port=5432,
    )


def close_connection_pool():
    global app
    app.state.connection_pool.closeall()


app = FastAPI()
app.add_event_handler('startup', get_connection_pool)
app.add_event_handler('shutdown', close_connection_pool)


@app.get('/hello')
def hello(name: Optional[str] = None):
    return {'message': f'Hello {name or "World"}!'}


@app.get('/hello_ujson')
def hello_ujson(name: Optional[str] = None):
    return UJSONResponse({'message': f'Hello {name or "World"}!'})


@app.get('/db')
def db(name: Optional[str] = None):
    pool = app.state.connection_pool
    conn = pool.getconn()
    cur = conn.cursor()
    if name:
        cur.execute(query_by_name, (name,))
    else:
        cur.execute(query_all)
    items = cur.fetchall()
    pool.putconn(conn)
    result = []
    for item in items:
        result.append({
            'student_id': item[0],
            'student_name': item[1],
            'student_gender': item[2],
            'student_birthday': item[3],
        })
    return result


@app.get('/numpy')
def numpy():
    arr = np.random.random([1000, 1000])
    core = np.random.random([18, 18])
    conv = signal.convolve2d(arr, core)
    l1 = conv.mean(axis=0).tolist()
    l2 = conv.mean(axis=1).tolist()
    return {'l1': l1, 'l2': l2}


if __name__ == '__main__':
    uvicorn.run(app=app, port=8080)
