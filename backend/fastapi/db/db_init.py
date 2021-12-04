from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

HOST = "db"
DB_NAME = "sample_db"
USER = "user"
PASSWORD = "password"

SQLALCHEMY_DATABASE_URL = f"mysql://{USER}:{PASSWORD}@{HOST}/{DB_NAME}?charset=utf8"

ENGINE = create_engine(
        SQLALCHEMY_DATABASE_URL,
        encoding = "utf-8",
        echo = True
)

SessionLocal = scoped_session(
    sessionmaker(
        autocommit = False,
        autoflush = False,
        bind = ENGINE
    )
)

Base = declarative_base()
Base.query = SessionLocal.query_property()
