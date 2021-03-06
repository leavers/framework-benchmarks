import logging

import numpy as np
import uvicorn
from psycopg2.pool import ThreadedConnectionPool
from scipy import signal
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from starlette.routing import Route
from ujson import dumps as ujson_dumps

logging.disable()

query_by_name = '''select student_id, student_name, student_gender, student_birthday 
from test.sc_student where student_name = %s'''

query_all = 'select student_id, student_name, student_gender, student_birthday from test.sc_student'


class UJSONResponse(Response):
    media_type = "application/json"

    def render(self, content) -> bytes:
        return ujson_dumps(content).encode("utf-8")


def setup_connection_pool():
    app.state.connection_pool = ThreadedConnectionPool(
        minconn=16,
        maxconn=16,
        database='test',
        user='postgres',
        password='123456',
        host='127.0.0.1',
        port=5432,
    )


def teardown_connection_pool(*args, **kwargs):
    app.state.connection_pool.closeall()


def hello(request: Request):
    name = request.query_params.get('name', 'World')
    return JSONResponse({'message': f'Hello {name}!'})


def hello_ujson(request: Request):
    name = request.query_params.get('name', 'World')
    return UJSONResponse({'message': f'Hello {name}!'})


def db(request: Request):
    name = request.query_params.get('name')
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
            'student_birthday': item[3].strftime('%Y-%m-%d'),
        })
    return JSONResponse(result)


def numpy(_):
    arr = np.random.random([1000, 1000])
    core = np.random.random([18, 18])
    conv = signal.convolve2d(arr, core)
    l1 = conv.mean(axis=0).tolist()
    l2 = conv.mean(axis=1).tolist()
    return JSONResponse({'l1': l1, 'l2': l2})


app = Starlette(
    routes=[
        Route('/hello', hello),
        Route('/hello_ujson', hello_ujson),
        Route('/db', db),
        Route('/numpy', numpy),
    ],
    on_startup=[setup_connection_pool],
    on_shutdown=[teardown_connection_pool],
)

if __name__ == '__main__':
    uvicorn.run(app=app, port=8080)
