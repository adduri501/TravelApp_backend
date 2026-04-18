from app.orm.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Float, DateTime, Date, ForeignKey
from datetime import datetime, date
import uuid
from app.config import settings
from sqlalchemy.orm import relationship


class TripTable(Base):
    __tablename__ = "trip_table"
    __table_args__ = {"schema": settings.DB_SCHEMA}

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    name: Mapped[str] = mapped_column(String(255))

    vehicle_number: Mapped[str] = mapped_column(
        ForeignKey(f"{settings.DB_SCHEMA}.vehicle_table.vehicle_number")
    )
    vehicle = relationship("VehicleTable", back_populates="trips")
    starting_date: Mapped[date] = mapped_column(Date)
    starting_time: Mapped[datetime] = mapped_column(DateTime)

    available_seats: Mapped[int] = mapped_column(Integer)
    amount: Mapped[float] = mapped_column(Float)

    from_location: Mapped[str] = mapped_column(String(255), nullable=True)
    to_location: Mapped[str] = mapped_column(String(255), nullable=True)
    
    driver_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(f"{settings.DB_SCHEMA}.driver_table.id"),
        nullable=True
    )
    status: Mapped[str] = mapped_column(String(255), nullable=True, default=None)

    driver = relationship("DriverTable", back_populates="trips")