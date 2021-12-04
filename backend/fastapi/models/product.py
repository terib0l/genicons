from sqlalchemy import Column, LargeBinary
from sqlalchemy_utils import UUIDType
from uuid import uuid4

from db.db_init import Base

class ProductTable(Base):
    """
    Producted images by app
    """
    __tablename__ = 'product'

    id = Column(UUIDType(binary=False), default=uuid4, primary_key=True)
    rounded_square_icon = Column(LargeBinary(length=(2**24)))
    circle_icon = Column(LargeBinary(length=(2**24)))
