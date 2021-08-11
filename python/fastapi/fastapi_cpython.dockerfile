# docker build . -f fastapi_cpython.dockerfile -t fastapi_cpython:latest

FROM python:3.9

WORKDIR /usr/src/app
ADD . .

RUN apt-get update && \
    apt-get -y install libpq-dev && \
    pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir \
                asyncpg fastapi gunicorn meinheld numpy psycopg2 scipy ujson uvicorn\[standard\] uwsgi

EXPOSE 8080

CMD [ "gunicorn", "app:app", "-b", "0.0.0.0:8080", "-w", "4", "-k", "uvicorn.workers.UvicornWorker" ]

