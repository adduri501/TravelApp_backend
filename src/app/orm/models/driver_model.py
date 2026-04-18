from app.orm.models.base import Base
from app.config import settings
from sqlalchemy import (
    Table,
    Column,
    ForeignKey,
    UniqueConstraint,
    String,
    Text,
    text,
    DateTime,
    func,
    Float,
)
from sqlalchemy.orm import relationship
from datetime import datetime


from sqlalchemy import String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
import uuid

from app.config import settings
from app.common.constant import DRIVER_TABLE


class DriverTable(Base):
    __tablename__ = DRIVER_TABLE
    __table_args__ = {"schema": settings.DB_SCHEMA}

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(f"{settings.DB_SCHEMA}.user_table.id"),
        nullable=False,
        unique=True,  # 🔥 one user = one driver profile
    )
    

    name: Mapped[str] = mapped_column(String(255), nullable=True)

    license_number: Mapped[str] = mapped_column(String(100), nullable=True, unique=True)

    vehicle_number: Mapped[str] = mapped_column(String(50), nullable=True)

    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)

    address: Mapped[str] = mapped_column(String(500), nullable=True)

    aadhaar_number: Mapped[str] = mapped_column(String(20), nullable=True, unique=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    user = relationship("UserTable", back_populates="driver")
