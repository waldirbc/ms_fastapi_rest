from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    price: float
    quantity: int
    category: str


class ProductCreate(ProductBase):
    pass


class ProductRead(ProductBase):
    id: int
    creation_date: datetime

    class Config:
        orm_mode = True


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
    category: Optional[str] = None
