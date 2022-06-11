from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from app.core.config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD

SQLALCHEMY_DATABASE_URL = (
    f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}?charset=utf8"
)

ENGINE = create_engine(SQLALCHEMY_DATABASE_URL, encoding="utf-8", echo=False)

SessionLocal = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)
)

Base = declarative_base()
Base.query = SessionLocal.query_property()
