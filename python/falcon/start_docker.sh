#!/bin/bash

set -e

docker run --rm --name=falcon_cpython_gevent --net=host --cpus=4 falcon_cpython_gevent:latest \
  gunicorn app_wsgi:app -b 0.0.0.0:8080 -w 4
docker run --rm --name=falcon_cpython_gevent --net=host --cpus=4 falcon_cpython_gevent:latest \
  gunicorn app_wsgi:app -b 0.0.0.0:8080 -w 4 -k gevent
docker run --rm --name=falcon_cpython_meinheld --net=host --cpus=4 falcon_cpython_meinheld:latest \
  gunicorn app_wsgi:app -b 0.0.0.0:8080 -w 4 -k egg:meinheld#gunicorn_worker
docker run --rm --name=falcon_pypy_meinheld --net=host --cpus=4 falcon_pypy_meinheld:latest \
  gunicorn app_wsgi:app -b 0.0.0.0:8080 -w 4 -k egg:meinheld#gunicorn_worker
docker run --rm --name=falcon_cpython_gevent --net=host --cpus=4 falcon_cpython_gevent:latest \
  gunicorn app_asgi:app -b 0.0.0.0:8080 -w 4 -k uvicorn.workers.UvicornWorker
docker run --rm --name=falcon_cpython_gevent --net=host --cpus=4 falcon_cpython_gevent:latest \
  gunicorn app_asgi:app -b 0.0.0.0:8080 -w 4 -k uvicorn.workers.UvicornH11Worker
# meinheld is not compatible with asgi
