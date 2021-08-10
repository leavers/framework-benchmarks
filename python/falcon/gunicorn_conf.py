import multiprocessing
import sys

workers = int(multiprocessing.cpu_count() * 2 + 1)
bind = "0.0.0.0:8080"
keepalive = 120
errorlog = "-"
pidfile = "gunicorn.pid"

if hasattr(sys, "pypy_version_info"):
    worker_class = "sync"
