from pydantic import BaseModel, Field

class Product(BaseModel):
    id: int = Field(None)
    rounded_square_icon: bytes
    circle_icon: bytes

    class Config:
        orm_mode = True
