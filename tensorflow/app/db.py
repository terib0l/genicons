import io
from PIL import Image
from uuid import uuid4
from pydantic import UUID4
from sqlalchemy import create_engine, Column, ForeignKey, update
from sqlalchemy.orm import sessionmaker, Session, relationship
from sqlalchemy.types import String, LargeBinary, Integer, BOOLEAN
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import UUIDType

from app.config import (
    MYSQL_HOST,
    MYSQL_NAME,
    MYSQL_USER,
    MYSQL_PASSWORD,
)

DATABASE_URL = f"mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_NAME}?charset=utf8"

ENGINE = create_engine(
    DATABASE_URL,
    encoding="utf-8",
    echo=False,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    password = Column(String(60), nullable=False)
    email = Column(String(255), nullable=False)
    premium = Column(BOOLEAN, default=False)

    products = relationship("Product")


class Product(Base):
    __tablename__ = "products"

    product_id = Column(UUIDType(binary=False), default=uuid4, primary_key=True)
    origin_img = Column(LargeBinary(length=(2**24)), nullable=False)
    rounded_square_icon = Column(LargeBinary(length=(2**24)))
    circle_icon = Column(LargeBinary(length=(2**24)))

    users_id = Column(Integer, ForeignKey("users.id"))


def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def create_rounded_square_icon(
    session: Session,
    image: Image.Image,
    product_id: UUID4
) -> None:
    imgdata = io.BytesIO()
    image.save(imgdata, "PNG")
    imgdata.seek(0)
    imgfile = imgdata.read()

    statement = update(Product).where(Product.product_id == product_id).\
            values(rounded_square_icon=imgfile)
    session.execute(statement)
    session.commit()


def create_circle_icon(
    session: Session,
    image: Image.Image,
    product_id: UUID4
) -> None:
    imgdata = io.BytesIO()
    image.save(imgdata, "PNG")
    imgdata.seek(0)
    imgfile = imgdata.read()

    statement = update(Product).where(Product.product_id == product_id).\
            values(circle_icon=imgfile)
    session.execute(statement)
    session.commit()

