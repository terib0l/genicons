from sqlalchemy import Column, LargeBinary, Integer
from sqlalchemy.orm import relationship

from db.db_init import Base

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    rounded_square_icon = Column(LargeBinary(length=(2**24)))
    circle_icon = Column(LargeBinary(length=(2**24)))

    owner = relationship("User", back_populates="products")
