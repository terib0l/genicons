# Ref: https://sqlalchemy-utils.readthedocs.io/en/latest/_modules/sqlalchemy_utils/types/uuid.html

from sqlalchemy import Column, String, LargeBinary
from sqlalchemy_utils import UUIDType
from uuid import uuid4

from .db_config import Base

class InitializeTable(Base):
    """About uuid in MySQL
    UUID Types are BINARY(16) or CHAR(32) in MySQL.
    My config "binary=False" shows CHAR(32).
    """
    __tablename__ = 'user'

    user_id = Column(UUIDType(binary=False), default=uuid4, primary_key=True)
    img = Column(LargeBinary(length=(2**24)), nullable=False) # size = MEDIUMBLOB
    img_name = Column(String(20), nullable=False)

class ProductedTable(Base):
    """
    Producted images by app
    """
    __tablename__ = 'product'

    id = Column(UUIDType(binary=False), default=uuid4)
    rounded_square_icon = Column(LargeBinary(length=(2**24))
    circle_icon = Column(LargeBinary(length=(2**24))
