"""
otp_table
---------
id
mobile_number   (or email)
otp
expires_at
is_used
attempt_count   (optional but useful)
created_at"""

from app.orm.models.base import Base
from app.common.constant import OTP_TABLE
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, DateTime, func, Boolean, Integer
import uuid
from datetime import datetime

from sqlalchemy.orm import mapped_column, Mapped
from app.config import settings

class OtpTable(Base):
    __tablename__ = OTP_TABLE
    __table_args__ = {"schema": settings.DB_SCHEMA}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    mobile_number: Mapped[str] = mapped_column(String(25), nullable=False)
    otp: Mapped[str] = mapped_column(String(6), nullable=False)
    expire_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    is_used: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    attempted_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
