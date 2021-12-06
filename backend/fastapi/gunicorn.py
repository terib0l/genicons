import re
import multiprocessing

name = "genicons"

bind = "localhost:8888"

worker_class = "uvicorn.workers.UvicornWorker"
workers = multiprocessing.cpu_count() * 2 + 1
thread = multiprocessing.cpu_count() * 2 + 1

#user = ""
#group = ""

accesslog = "/var/log/gunicorn/access.log"
errorlog = "/var/log/gunicorn/error.log"

reload = True
#daemon = True

raw_env = []
with open(".env", "r") as envs:
    while env := envs.readline():
        raw_env.append(re.sub("\n", "", env))
