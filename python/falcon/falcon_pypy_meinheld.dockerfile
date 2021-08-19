# docker build . -f falcon_pypy_meinheld.dockerfile -t falcon_pypy_meinheld:latest

FROM pypy:3.7

WORKDIR /usr/src/app
ADD . .

RUN apt-get update && \
    apt-get -y install libpq-dev && \
    pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir \
                falcon \
                gunicorn \
                meinheld \
                psycopg2cffi \
                ujson \
                uvicorn

EXPOSE 8080

CMD [ "gunicorn", "app_wsgi:app", "-b", "0.0.0.0:8080", "-w", "4" ]

