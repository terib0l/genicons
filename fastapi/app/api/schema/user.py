from typing import List, Optional
from pydantic import EmailStr
from pydantic import BaseModel

from app.api.schema.product import Product


class User(BaseModel):
    id: Optional[int] = None
    name: str
    email: EmailStr
    premium: bool = False

    products: Optional[List[Product]] = None

    class Config:
        orm_mode = True
