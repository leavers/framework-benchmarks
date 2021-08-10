from flask import Flask, jsonify, request

import logging

logging.disable()

app = Flask('flask')


@app.route('/hello')
def hello():
    name = request.args.get('name') or 'World'
    return jsonify(message=f'Hello {name}!')


@app.route('/async/hello')
async def async_hello():
    name = request.args.get('name') or 'World'
    return jsonify(message=f'Hello {name}!')


if __name__ == '__main__':
    app.run(port=8080, debug=True)
