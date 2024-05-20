import datetime
from pydantic import BaseModel


class PurchaseSchema(BaseModel):
    id: int
    date: datetime.datetime
    cost: int
    seller_id: int
