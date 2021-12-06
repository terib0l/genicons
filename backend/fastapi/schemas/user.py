from typing import List
from pydantic import BaseModel, Field
#from pydantic import StrictBytes
from pydantic.types import UUID4

from product import Product

class User(BaseModel):
    id: UUID4
    img: bytes
    img_name: str = Field(..., max_length=20)
    products: List[Product] = []

    class Config:
        orm_mode = True
