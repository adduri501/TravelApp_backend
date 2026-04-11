from app.orm.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column
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
from app.config import settings
from sqlalchemy.orm import relationship
import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from app.common.constant import DEVICE_TABLE


class DeviceTable(Base):
    __tablename__ = DEVICE_TABLE
    __table_args__ = {"schema": settings.DB_SCHEMA}
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(f"{settings.DB_SCHEMA}.user_table.id"), nullable=False
    )
    device: Mapped[str] = mapped_column(String(254), nullable=True)
    device_token: Mapped[str] = mapped_column(String(1000), nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=True)
    longitude: Mapped[float] = mapped_column(Float, nullable=True)
    last_login: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    user = relationship("UserTable", back_populates="devices")

    refresh_tokens = relationship("RefreshTokenTable", backref="device")
