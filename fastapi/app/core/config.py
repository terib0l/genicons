from starlette.config import Config
from starlette.datastructures import Secret

config = Config(".env")

PROJECT_NAME = "Genicons"
VERSION = "1.0.0"
DEBUG = True

MYSQL_HOST = config("MYSQL_HOST", cast=str, default="localhost")
MYSQL_NAME = config("MYSQL_NAME", cast=str, default="sample_db")
MYSQL_USER = config("MYSQL_USER", cast=str, default="user")
MYSQL_PASSWORD = config("MYSQL_PASSWORD", cast=Secret, default="password")
