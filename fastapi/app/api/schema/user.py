from typing import List
from pydantic import EmailStr
from pydantic import BaseModel

from app.api.schema.product import Product


class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    premium: bool

    products: List[Product]

    class Config:
        orm_mode = True
