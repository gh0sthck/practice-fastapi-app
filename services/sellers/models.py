import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import String
from database import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from services.purchases.models import Purchase


class Seller(Base):
    __tablename__ = "seller"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(127), nullable=False)
    last_name: Mapped[str] = mapped_column(String(127), unique=True, nullable=False)
    birthday: Mapped[datetime.date]
    
    purchases: Mapped[List["Purchase"]] = relationship(back_populates="seller")
