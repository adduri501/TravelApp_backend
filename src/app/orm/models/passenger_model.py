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
from datetime import datetime
import uuid
from sqlalchemy.orm import Mapped, mapped_column
from app.orm.models.base import Base
from sqlalchemy.orm import relationship
from app.common.constant import PASSENGER_TABLE
from app.config import settings
from sqlalchemy.dialects.postgresql import UUID


class PassengerTable(Base):
    __tablename__ = PASSENGER_TABLE
    __table_args__ = {"schema": settings.DB_SCHEMA}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(f"{settings.DB_SCHEMA}.user_table.id"), nullable=False
    )
    name:Mapped[str]=mapped_column(String(255),nullable=True)
    email:Mapped[str]=mapped_column(String(255),nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    user = relationship("UserTable", back_populates="passenger")

