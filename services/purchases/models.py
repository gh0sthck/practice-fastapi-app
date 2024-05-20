import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, func

from database import Base
from services.sellers.models import Seller


class Purchase(Base):
    __tablename__ = "purchase"

    id: Mapped[int] = mapped_column(primary_key=True)
    seller_id: Mapped[int] = mapped_column(ForeignKey("seller.id", ondelete="CASCADE"))
    cost: Mapped[int]
    date: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.now(),
        server_default=func.now()
    )

    seller: Mapped["Seller"] = relationship(back_populates="purchases")
