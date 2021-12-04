import multiprocessing

name = "genicons"

bind = "localhost:8888"

worker_class = "uvicorn.workers.UvicornWorker"
workers = multiprocessing.cpu_count() * 2 + 1
thread = multiprocessing.cpu_count() * 2 + 1

raw_env = []

#user = ""
#group = ""

accesslog = "/var/log/gunicorn/access.log"
errorlog = "/var/log/gunicorn/error.log"

reload = True
#daemon = True
