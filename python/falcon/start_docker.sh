#!/bin/bash

set -e

# command of building image:
# docker build . -f falcon_cpython.dockerfile -t falcon_cpython:latest
docker run --rm --name=falcon_cpython --net=host --cpus=4 falcon_cpython:latest \
  gunicorn app_wsgi:app -b 0.0.0.0:8080 -w 4
docker run --rm --name=falcon_cpython --net=host --cpus=4 falcon_cpython:latest \
  gunicorn app_asgi:app -b 0.0.0.0:8080 -w 4 -k uvicorn.workers.UvicornWorker

