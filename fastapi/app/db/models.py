from sqlalchemy import Column, String, LargeBinary, Integer, ForeignKey
from sqlalchemy_utils import UUIDType
from sqlalchemy.orm import relationship
from uuid import uuid4

from app.db.db_init import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUIDType(binary=False), default=uuid4, primary_key=True)
    img = Column(LargeBinary(length=(2**24)), nullable=False)
    img_name = Column(String(20), nullable=False)

    products = relationship("Product")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    rounded_square_icon = Column(LargeBinary(length=(2**24)))
    circle_icon = Column(LargeBinary(length=(2**24)))

    users_id = Column(UUIDType(binary=False), ForeignKey("users.id"), default=uuid4)
