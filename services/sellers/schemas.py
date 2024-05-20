import datetime
from pydantic import BaseModel, Field


class SellerSchema(BaseModel):
    id: int
    first_name: str = Field(le=127)
    last_name: str = Field(le=127)
    sallary: int
    phone: str = Field(le=50)
    is_personal: bool = Field(default=False)
    birthday: datetime.date


class SellerUpdateSchema(BaseModel):
    first_name: str = Field(le=127)
    last_name: str = Field(le=127)
    sallary: int
    phone: str = Field(le=50)
    is_personal: bool = Field(default=False)
    birthday: datetime.date
