#!/bin/bash

set -e

docker run --rm --name=fastapi_cpython --net=host --cpus=4 fastapi_cpython:latest \
  gunicorn app:app -b 0.0.0.0:8080 -w 4 -k uvicorn.workers.UvicornWorker
docker run --rm --name=fastapi_cpython --net=host --cpus=4 fastapi_cpython:latest \
  gunicorn app:app -b 0.0.0.0:8080 -w 4 -k uvicorn.workers.UvicornH11Worker
docker run --rm --name=fastapi_cpython --net=host --cpus=4 fastapi_cpython:latest \
  gunicorn async_app:app -b 0.0.0.0:8080 -w 4 -k uvicorn.workers.UvicornWorker
docker run --rm --name=fastapi_cpython --net=host --cpus=4 fastapi_cpython:latest \
  gunicorn async_app:app -b 0.0.0.0:8080 -w 4 -k uvicorn.workers.UvicornH11Worker
# meinheld is not compatible with asgi