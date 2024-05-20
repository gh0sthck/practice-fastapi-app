from pydantic import BaseModel


class CategorySchema(BaseModel):
    id: int
    name: str


class CategoryUpdateSchema(BaseModel):
    name: str
