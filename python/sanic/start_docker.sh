#!/bin/bash

set -e

docker run --rm --name=sanic_cpython --net=host --cpus=4 sanic_cpython:latest \
  sanic app:app -H 0.0.0.0 -p 8080 -w 4 --no-access-logs
docker run --rm --name=sanic_cpython --net=host --cpus=4 sanic_cpython:latest \
  sanic async_app:app -H 0.0.0.0 -p 8080 -w 4 --no-access-logs
# meinheld is not compatible with asgi