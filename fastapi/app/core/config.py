import subprocess
from pydantic import EmailStr
from starlette.config import Config
from starlette.datastructures import Secret

config = Config(".env")

PROJECT_NAME = "Genicons"
VERSION = "1.0.0"
DEBUG = True

MYSQL_HOST = config("MYSQL_HOST", cast=str, default="127.0.0.1")
MYSQL_NAME = config("MYSQL_NAME", cast=str, default="sample_db")
MYSQL_USER = config("MYSQL_USER", cast=str, default="user")
MYSQL_PASSWORD = config("MYSQL_PASSWORD", cast=Secret, default="password")

MANAGEMENT_EMAIL = config("MANAGEMENT_EMAIL", cast=EmailStr)
MANAGEMENT_EMAIL_PASSWD = config("MANAGEMENT_EMAIL_PASSWD", cast=Secret)

SECRET_KEY = config(
    "SECRET_KEY",
    cast=Secret,
    default=subprocess.run(
        ["openssl", "rand", "-hex", "32"], stdout=subprocess.PIPE, text=True
    ).stdout[:-1],
)
ALGORITHM = config("ALGORITHM", cast=str, default="HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = config(
    "ACCESS_TOKEN_EXPIRE_MINUTES", cast=int, default=30
)
