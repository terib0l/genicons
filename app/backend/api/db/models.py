# Ref: https://sqlalchemy-utils.readthedocs.io/en/latest/_modules/sqlalchemy_utils/types/uuid.html

from sqlalchemy import Column, Integer, String
from sqlalchemy_utils import UUIDType
from uuid import uuid4

from .database import Base

class SampleTable(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, AUTO_INCREMENT=True)
    # DATABASE=MySQL => BINARY(16) or CHAR(32)
    # binary=False    => CHAR(32)
    uuid = Column(UUIDType(binary=False), default=uuid4, unique=True, nullable=False)
    title = Column(String(20), nullable=False)
    icon = Column(String(30), nullable=False)
