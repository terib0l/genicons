from starlette.config import Config
from starlette.datastructures import Secret

config = Config(".env")

PROJECT_NAME = "Genicons"
VERSION = "1.0.0"
DEBUG = True

DB_HOST = config("DB_HOST", cast=str, default="127.0.0.1")
DB_NAME = config("DB_NAME", cast=str, default="sample_db")
DB_USER = config("DB_USER", cast=str, default="user")
DB_PASSWORD = config("DB_PASSWORD", cast=Secret, default="password")
