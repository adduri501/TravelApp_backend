from app.orm.models.base import Base
from sqlalchemy import Column, Float, ForeignKey
from app.config import settings

class WalletTable(Base):
    __tablename__ = "wallet_table"
    __table_args__ = {"schema": settings.DB_SCHEMA}

    user_id = Column(
        ForeignKey(f"{settings.DB_SCHEMA}.user_table.id"),
        primary_key=True
    )
    balance = Column(Float, default=0)