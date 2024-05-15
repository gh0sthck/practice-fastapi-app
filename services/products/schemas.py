from pydantic import BaseModel


class ProductSchema(BaseModel):
    id: int
    name: str
    count: int
    category_id: int
    
