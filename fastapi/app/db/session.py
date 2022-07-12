from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from app.core.config import DATABASE_URL

SQLALCHEMY_DATABASE_URL = DATABASE_URL

ENGINE = create_engine(SQLALCHEMY_DATABASE_URL, encoding="utf-8", echo=True)

db_session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=ENGINE,
    )
)

Base = declarative_base()
Base.query = db_session.query_property()


def get_db():
    session = db_session()
    try:
        yield session
    except Exception:
        session.rollback()
    finally:
        session.close()
