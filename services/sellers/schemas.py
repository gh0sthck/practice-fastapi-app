import datetime
from pydantic import BaseModel, Field


class SellerSchema(BaseModel):
    id: int
    first_name: str = Field(max_length=127)
    last_name: str = Field(max_length=127)
    sallary: int
    phone: str = Field(max_length=50)
    is_personal: bool = Field(default=False)
    birthday: datetime.date


class SellerUpdateSchema(BaseModel):
    first_name: str = Field(max_length=127)
    last_name: str = Field(max_length=127)
    sallary: int
    phone: str = Field(max_length=50)
    is_personal: bool = Field(default=False)
    birthday: datetime.date
