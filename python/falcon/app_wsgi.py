import atexit
import logging
from json import dumps as json_dumps
from wsgiref.simple_server import make_server

import falcon
import numpy as np
from falcon.request import Request
from falcon.response import Response
from psycopg2.pool import ThreadedConnectionPool
from scipy import signal
from ujson import dumps as ujson_dumps

logging.disable()

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


class HelloResource:

    def on_get(self, req: Request, resp: Response):
        name = req.params.get('name') or 'World'
        resp.status = falcon.HTTP_200
        resp.content_type = falcon.MEDIA_JSON
        resp.text = json_dumps({'message': f'Hello {name}!'})


class HelloUJsonResource:

    def on_get(self, req: Request, resp: Response):
        name = req.params.get('name') or 'World'
        resp.status = falcon.HTTP_200
        resp.content_type = falcon.MEDIA_JSON
        resp.text = ujson_dumps({'message': f'Hello {name}!'})


class DatabaseResource:

    def on_get(self, req: Request, resp: Response):
        name = req.params.get('name')
        global connection_pool
        conn = connection_pool.getconn()
        cur = conn.cursor()
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
        resp.text = json_dumps(result)


class NumpyResource:

    def on_get(self, _: Request, resp: Response):
        arr = np.random.random([1000, 1000])
        core = np.random.random([18, 18])
        conv = signal.convolve2d(arr, core)
        l1 = conv.mean(axis=0).tolist()
        l2 = conv.mean(axis=1).tolist()
        resp.text = json_dumps({'l1': l1, 'l2': l2})


app = falcon.App()
app.add_route('/hello', HelloResource())
app.add_route('/hello_ujson', HelloUJsonResource())
app.add_route('/db', DatabaseResource())
app.add_route('/numpy', NumpyResource())

if __name__ == '__main__':
    with make_server('', 8080, app) as httpd:
        print('Serving on port 8080...')
        httpd.serve_forever()
