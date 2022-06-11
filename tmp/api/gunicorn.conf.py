import yaml
import multiprocessing

wsgi_app = "main:app"

bind = "0.0.0.0:8888"

worker_class = "uvicorn.workers.UvicornWorker"
workers = multiprocessing.cpu_count() * 2 + 1
# thread =

accesslog = "/var/log/gunicorn/access.log"
errorlog = "/var/log/gunicorn/error.log"

loglevel = "debug"
with open("./logging.yaml", "r") as conf:
    LOGGING = yaml.safe_load(conf)

reload = True
daemon = True

"""
import re
raw_env = []
with open("../.env", "r") as envs:
    while env := envs.readline():
        raw_env.append(re.sub("\n", "", env))
"""
