# Framework Benchmarks

This project aims to perform performance tests on several common Python web frameworks and server deployment solutions, so as to have a more concrete understanding of the differences between different combinations.

There are currently three test items: a simple "Hello World" interface, querying data from a PostgreSQL database, and returning results after matrix operations based on scipy/numpy.

Frameworks I tested:

- bottle
- falcon
- fastapi
- flask
- sanic
- starlette

Some conclusions based on my "rough" experiments:

1. Falcon (WSGI) + CPython + Meinheld performs much better than others on my PC;
2. Meinheld brings WSGI comparable (or even better) performance improvements to ASGI in IO tasks;
3. PyPy is comparable with CPython + gevent or meinheld, and better than bare CPython. 