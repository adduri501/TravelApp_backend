from app.orm.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, Float, ForeignKey, DateTime, String
from sqlalchemy import String, Boolean, Float
from typing import Optional
from datetime import datetime
import uuid
from app.config import settings


class BookingTable(Base):
    __tablename__ = "booking_table"
    __table_args__ = {"schema": settings.DB_SCHEMA}

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(f"{settings.DB_SCHEMA}.user_table.id")
    )

    trip_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(f"{settings.DB_SCHEMA}.trip_table.id")
    )

    seats_booked: Mapped[int] = mapped_column(Integer)
    total_amount: Mapped[float] = mapped_column(Float)
    
    transaction_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    coupon_applied: Mapped[bool] = mapped_column(Boolean, default=False)

    coupon_code: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    discount_amount: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

  

    status: Mapped[str] = mapped_column(default="booked")

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)