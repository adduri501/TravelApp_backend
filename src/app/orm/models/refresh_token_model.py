from app.orm.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, Boolean, ForeignKey
import uuid
from datetime import datetime
from app.config import settings
from app.common.constant import REFRESH_TOKEN_TABLE,DEVICE_TABLE,USER_TABLE


class RefreshTokenTable(Base):
    __tablename__ = REFRESH_TOKEN_TABLE
    __table_args__ = {"schema": settings.DB_SCHEMA}

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(f"{settings.DB_SCHEMA}.{USER_TABLE}.id"), nullable=False
    )
    device_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(f"{settings.DB_SCHEMA}.{DEVICE_TABLE}.id"), nullable=False
    )
    token_jti: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    is_revoked: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )


