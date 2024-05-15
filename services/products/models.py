from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String

from database import Base

if TYPE_CHECKING:
    from categories.models import Category


class Product(Base):
    __tablename__ = "product"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    category: Mapped["Category"] = relationship(back_populates="products")
    count: Mapped[int]
    
