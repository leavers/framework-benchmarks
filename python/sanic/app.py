import logging
from json import dumps as json_dumps

import numpy as np
from psycopg2.pool import ThreadedConnectionPool
from sanic import Sanic
from sanic.request import Request
from sanic.response import json
from scipy import signal
from ujson import dumps as ujson_dumps

logging.disable()

query_by_name = '''select student_id, student_name, student_gender, student_birthday 
from test.sc_student where student_name = %s'''

query_all = 'select student_id, student_name, student_gender, student_birthday from test.sc_student'

app = Sanic(name='Sanic')


@app.after_server_start
def setup_connection_pool(*args, **kwargs):
    app.ctx.connection_pool = ThreadedConnectionPool(
        minconn=16,
        maxconn=16,
        database='test',
        user='postgres',
        password='123456',
        host='127.0.0.1',
        port=5432,
    )


@app.before_server_stop
def teardown_connection_pool(*args, **kwargs):
    app.ctx.connection_pool.closeall()


@app.get('/hello')
def hello(request: Request):
    name = request.args.get('name', 'World')
    return json({'message': f'Hello {name}!'}, dumps=json_dumps)


@app.get('/hello_ujson')
def hello_ujson(request: Request):
    name = request.args.get('name', 'World')
    return json({'message': f'Hello {name}!'}, dumps=ujson_dumps)


@app.get('/db')
def db(request: Request):
    name = request.args.get('name')
    pool = app.ctx.connection_pool
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
    return json(result)


@app.get('/numpy')
def numpy(_):
    arr = np.random.random([1000, 1000])
    core = np.random.random([18, 18])
    conv = signal.convolve2d(arr, core)
    l1 = conv.mean(axis=0).tolist()
    l2 = conv.mean(axis=1).tolist()
    return json({'l1': l1, 'l2': l2})


if __name__ == '__main__':
    app.run(port=8080)
