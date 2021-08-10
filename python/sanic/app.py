from sanic import Sanic
from sanic.request import Request
from sanic.response import json

from json import dumps as json_dumps
from ujson import dumps as ujson_dumps

app = Sanic('app')


@app.get('/hello')
def hello(request: Request):
    name = request.args.get('name') or 'World'
    return json({'message': f'Hello {name}!'}, dumps=json_dumps)


@app.get('/hello_ujson')
def hello_ujson(request: Request):
    name = request.args.get('name') or 'World'
    return json({'message': f'Hello {name}!'}, dumps=ujson_dumps)


@app.get('/async/hello')
async def async_hello(request: Request):
    name = request.args.get('name') or 'World'
    return json({'message': f'Hello {name}!'}, dumps=json_dumps)


@app.get('/async/hello_ujson')
async def async_hello_usjon(request: Request):
    name = request.args.get('name') or 'World'
    return json({'message': f'Hello {name}!'}, dumps=ujson_dumps)


if __name__ == '__main__':
    app.run(port=8080)
