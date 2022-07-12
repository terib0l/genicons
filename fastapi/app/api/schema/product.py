from pydantic import BaseModel
from pydantic.types import UUID4


class Product(BaseModel):
    product_id: UUID4
    origin_img: bytes
    rounded_square_icon: bytes
    circle_icon: bytes

    # ForeignKey
    users_id: int

    class Config:
        orm_mode = True
