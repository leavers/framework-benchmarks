import atexit
from bottle import Bottle, request, response

from psycopg2.pool import ThreadedConnectionPool
import numpy as np
from scipy import signal
from json import dumps as json_dumps
from ujson import dumps as ujson_dumps

query_by_name = '''select student_id, student_name, student_gender, student_birthday 
from test.sc_student where student_name = %s'''

query_all = 'select student_id, student_name, student_gender, student_birthday from test.sc_student'

connection_pool = ThreadedConnectionPool(
    minconn=16,
    maxconn=16,
    database='test',
    user='postgres',
    password='123456',
    host='127.0.0.1',
    port=5432,
)


@atexit.register
def close_connection_pool():
    global connection_pool
    connection_pool.closeall()


app = Bottle()


@app.get('/hello')
def hello():
    name = request.query.get('name', 'World')
    return {'message': f'Hello {name}!'}


@app.get('/hello_ujson')
def hello_ujson():
    name = request.query.get('name', 'World')
    response.content_type = 'application/json'
    return ujson_dumps({'message': f'Hello {name}!'})


@app.get('/db')
def db():
    global connection_pool
    conn = connection_pool.getconn()
    cur = conn.cursor()
    name = request.query.get('name')
    if name:
        cur.execute(query_by_name, (name,))
    else:
        cur.execute(query_all)
    items = cur.fetchall()
    connection_pool.putconn(conn)
    result = []
    for item in items:
        result.append({
            'student_id': item[0],
            'student_name': item[1],
            'student_gender': item[2],
            'student_birthday': item[3].strftime('%Y-%m-%d'),
        })
    response.content_type = 'application/json'
    return json_dumps(result)


@app.get('/numpy')
def numpy():
    arr = np.random.random([1000, 1000])
    core = np.random.random([18, 18])
    conv = signal.convolve2d(arr, core)
    l1 = conv.mean(axis=0).tolist()
    l2 = conv.mean(axis=1).tolist()
    return {'l1': l1, 'l2': l2}


if __name__ == '__main__':
    app.run(port=8080)
