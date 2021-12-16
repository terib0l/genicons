from pydantic import BaseModel

class Product(BaseModel):
    id: int
    rounded_square_icon: bytes
    circle_icon: bytes

    class Config:
        orm_mode = True
