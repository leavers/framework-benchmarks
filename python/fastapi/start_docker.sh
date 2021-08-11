#!/bin/bash

set -e

# command of building image:
# docker build . -f fastapi_cpython.dockerfile -t fastapi_cpython:latest
docker run --rm --name=falcon_cpython --net=host --cpus=4 fastapi_cpython:latest \
  gunicorn app:app -b 0.0.0.0:8080 -w 4 -k uvicorn.workers.UvicornWorker
docker run --rm --name=fastapi_cpython --net=host --cpus=4 fastapi_cpython:latest \
  gunicorn async_app:app -b 0.0.0.0:8080 -w 4 -k uvicorn.workers.UvicornWorker
