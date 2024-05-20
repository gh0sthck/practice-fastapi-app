import datetime
from pydantic import BaseModel


class PurchaseSchema(BaseModel):
    id: int
    date: datetime.datetime
    cost: int
    seller_id: int


class PurchaseAddSchema(BaseModel):
    id: int
    cost: int
    seller_id: int
