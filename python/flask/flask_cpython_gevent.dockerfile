# docker build . -f flask_cpython_gevent.dockerfile -t flask_cpython_gevent:latest

FROM python:3.9

WORKDIR /usr/src/app
ADD . .

RUN apt-get update && \
    apt-get -y install libpq-dev && \
    pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir \
                asyncpg \
                flask \
                gunicorn\[gevent\] \
                numpy \
                psycopg2 \
                scipy \
                ujson \
                uvicorn\[standard\]

EXPOSE 8080

CMD [ "gunicorn", "app:app", "-b", "0.0.0.0:8080", "-w", "4" ]
