from pydantic import BaseModel

from categories.schemas import Category



class Product(BaseModel):
    id: int
    name: str
    category: Category
    count: int
