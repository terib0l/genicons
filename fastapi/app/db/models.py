from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import String, LargeBinary, Integer, BOOLEAN
from sqlalchemy_utils import UUIDType
from sqlalchemy.orm import relationship
from uuid import uuid4

from app.db.session import Base


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
