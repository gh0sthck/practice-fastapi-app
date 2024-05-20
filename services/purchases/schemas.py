import datetime
from pydantic import BaseModel


class PurchaseSchema(BaseModel):
    id: int
    date: datetime.datetime
    seller_id: int


class PurchaseAddSchema(BaseModel):
    id: int
    seller_id: int


class PurchaseListSchema(BaseModel):
    id: int
    purchase_id: int
    product_id: int


class PurchaseUpdateSchema(BaseModel):
    seller_id: int
