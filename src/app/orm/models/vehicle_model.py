from app.orm.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, ForeignKey, DateTime, func
from datetime import datetime
import uuid
from app.config import settings
from app.common.constant import VEHICLE_TABLE


class VehicleTable(Base):
    __tablename__ = VEHICLE_TABLE
    __table_args__ = {"schema": settings.DB_SCHEMA}

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    
    

    vehicle_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    vehicle_name: Mapped[str] = mapped_column(String(255), nullable=True)
    color: Mapped[str] = mapped_column(String(50), nullable=True)
    no_of_seats: Mapped[int] = mapped_column(nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
    trips = relationship("TripTable", back_populates="vehicle")