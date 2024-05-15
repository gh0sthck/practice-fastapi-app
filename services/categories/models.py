from typing import TYPE_CHECKING, List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

if TYPE_CHECKING:
    from services.products.models import Product


class Category(Base):
    __tablename__ = "category"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    products: Mapped[List["Product"]] = relationship(back_populates="category")
    
