# docker build . -f flask_cpython_meinheld.dockerfile -t falcon_cpython_meinheld:latest

FROM python:3.9

WORKDIR /usr/src/app
ADD . .

RUN apt-get update && \
    apt-get -y install libpq-dev && \
    pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir \
                asyncpg \
                flask \
                gunicorn \
                meinheld \
                numpy \
                psycopg2 \
                scipy \
                ujson \
                uvicorn\[standard\]

EXPOSE 8080

CMD [ "gunicorn", "app_wsgi:app", "-b", "0.0.0.0:8080", "-w", "4" ]
