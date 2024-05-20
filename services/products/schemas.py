from pydantic import BaseModel


class ProductSchema(BaseModel):
    id: int
    name: str
    count: int
    cost: int 
    category_id: int
    
