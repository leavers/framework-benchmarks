#!/bin/bash

set -e

docker run --rm --name=bottle_cpython_gevent --net=host --cpus=4 bottle_cpython_gevent:latest \
  gunicorn app:app -b 0.0.0.0:8080 -w 4
docker run --rm --name=bottle_cpython_gevent --net=host --cpus=4 bottle_cpython_gevent:latest \
  gunicorn app:app -b 0.0.0.0:8080 -w 4 -k gevent
docker run --rm --name=bottle_cpython_meinheld --net=host --cpus=4 bottle_cpython_meinheld:latest \
  gunicorn app:app -b 0.0.0.0:8080 -w 4 -k egg:meinheld#gunicorn_worker
