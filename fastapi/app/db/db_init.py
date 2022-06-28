from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from app.core.config import MYSQL_HOST, MYSQL_NAME, MYSQL_USER, MYSQL_PASSWORD

SQLALCHEMY_DATABASE_URL = "mysql://{}:{}@{}/{}?charset=utf8".format(
    MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_NAME
)

ENGINE = create_engine(SQLALCHEMY_DATABASE_URL, encoding="utf-8", echo=True)

SessionLocal = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=ENGINE,
    )
)

Base = declarative_base()
Base.query = SessionLocal.query_property()
