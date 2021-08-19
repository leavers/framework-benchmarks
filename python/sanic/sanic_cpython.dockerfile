# docker build . -f sanic_cpython.dockerfile -t sanic_cpython:latest

FROM python:3.9

WORKDIR /usr/src/app
ADD . .

RUN apt-get update && \
    apt-get -y install libpq-dev && \
    pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir \
                asyncpg \
                sanic \
                gunicorn \
                numpy \
                psycopg2 \
                scipy \
                ujson \
                uvicorn\[standard\]

EXPOSE 8080

CMD [ "sanic", "app.app", "-H", "0.0.0.0", "-p", "8080", "-w", "4" ]

