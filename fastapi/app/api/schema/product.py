from typing import Optional
from pydantic import BaseModel, Field
from pydantic.types import UUID4


class Product(BaseModel):
    product_id: UUID4
    origin_img: bytes
    rounded_square_icon: Optional[bytes] = Field(None)
    circle_icon: Optional[bytes] = Field(None)

    # ForeignKey
    users_id: int

    class Config:
        orm_mode = True
