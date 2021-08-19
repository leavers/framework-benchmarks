import logging
from typing import Optional

import numpy as np
from flask import Flask, request, Response
from flask.json import jsonify
from scipy import signal
from ujson import dumps as ujson_dumps

"""
Currently I don't know how to setup and teardown an async database context correctly,
so this app doesn't provide db testing interfaces.
"""

logging.disable()

app = Flask('Flask')


@app.get('/hello')
async def async_hello(name: Optional[str] = None):
    return jsonify({'message': f'Hello {name or "World"}!'})


@app.get('/hello_ujson')
async def async_hello_ujson():
    name = request.args.get('name', 'World')
    return Response(
        response=ujson_dumps({'message': f'Hello {name}!'}),
        status=200,
        mimetype='application/json',
    )


@app.get('/numpy')
async def async_numpy():
    arr = np.random.random([1000, 1000])
    core = np.random.random([18, 18])
    conv = signal.convolve2d(arr, core)
    l1 = conv.mean(axis=0).tolist()
    l2 = conv.mean(axis=1).tolist()
    return {'l1': l1, 'l2': l2}


if __name__ == '__main__':
    app.run(port=8080, debug=True)
