from sqlalchemy import Column, String, LargeBinary
from sqlalchemy_utils import UUIDType
from sqlalchemy.orm import relationship
from uuid import uuid4

from db.db_init import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(UUIDType(binary=False), default=uuid4, primary_key=True)
    img = Column(LargeBinary(length=(2**24)), nullable=False) # size = MEDIUMBLOB
    img_name = Column(String(20), nullable=False)

    products = relationship("Product")
