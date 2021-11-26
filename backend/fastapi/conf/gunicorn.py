import multiprocessing

accesslog = "/var/log/gunicorn/access.log"
errorlog = "/var/log/gunicorn/error.log"

bind = "0.0.0.0:8080"

worker_class = "uvicorn.workers.UvicornWorker"
workers = multiprocessing.cpu_count() * 2 + 1
thread = multiprocessing.cpu_count() * 2 + 1
