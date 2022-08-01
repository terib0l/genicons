from starlette.config import Config
from starlette.datastructures import Secret

config = Config(".env")

PROJECT_NAME = "Genicons ML"
VERSION = "1.0.0"
DEBUG = True

MYSQL_HOST = config("MYSQL_HOST", cast=str, default="127.0.0.1")
MYSQL_NAME = config("MYSQL_NAME", cast=str, default="sample_db")
MYSQL_USER = config("MYSQL_USER", cast=str, default="user")
MYSQL_PASSWORD = config("MYSQL_PASSWORD", cast=Secret, default="password")

STYLE_IMAGE_URL = config("STYLE_IMAGE_URL", cast=str, default="./style/munch_style.jpg")
