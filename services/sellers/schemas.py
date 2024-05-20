import datetime
from pydantic import BaseModel, Field


class SellerSchema(BaseModel):
    id: int
    first_name: str = Field()
    last_name: str = Field()
    birthday: datetime.date
