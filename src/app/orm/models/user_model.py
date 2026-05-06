from app.orm.models.base import Base
from app.config import settings
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.common.constant import USER_TABLE
from sqlalchemy import Column, String

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


class UserTable(Base):
    __tablename__ = USER_TABLE
    __table_args__ = {"schema": settings.DB_SCHEMA}
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(255), nullable=True)
    mobile_number: Mapped[str] = mapped_column(String(25), unique=True, nullable=True)
    email: Mapped[str] = mapped_column(String(254), nullable=True)
    alternative_mobile_number: Mapped[str] = mapped_column(String(25), nullable=True)
    profile_pic: Mapped[str] = mapped_column(String(500), nullable=True)
    gender: Mapped[str] = mapped_column(String(20), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=True)
    role: Mapped[str] = mapped_column(String(50), nullable=True)
    referral_code: Mapped[str] = mapped_column(String(20), unique=True, nullable=True)
    referred_by: Mapped[str] = mapped_column(String(20), nullable=True)
    devices = relationship("DeviceTable", back_populates="user")
    refresh_tokens = relationship("RefreshTokenTable", backref="user")
    passenger = relationship("PassengerTable", back_populates="user", uselist=False)
    driver = relationship("DriverTable", back_populates="user", uselist=False)


