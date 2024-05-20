import datetime
from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Column, ForeignKey, Table, func

from database import Base
from services.sellers.models import Seller
from services.products.models import Product


purchase_list = Table(
    "purchase_list",
    Base.metadata,
    Column("purchase", ForeignKey("purchase.id")),
    Column("product", ForeignKey("product.id"))
)


class Purchase(Base):
    __tablename__ = "purchase"

    id: Mapped[int] = mapped_column(primary_key=True)
    seller_id: Mapped[int] = mapped_column(ForeignKey("seller.id", ondelete="CASCADE"))
    date: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.now(),
        server_default=func.now()
    )
    products: Mapped[List["Product"]] = relationship(secondary=purchase_list)

    seller: Mapped["Seller"] = relationship(back_populates="purchases")
