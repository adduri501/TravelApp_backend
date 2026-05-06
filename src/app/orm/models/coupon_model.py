from app.orm.models.base import Base
from sqlalchemy import Column, String, Float, Integer, Boolean, DateTime
import uuid
from datetime import datetime
from app.config import settings

class CouponTable(Base):
    __tablename__ = "coupon_table"
    __table_args__ = {"schema": settings.DB_SCHEMA}

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    code = Column(String(50), unique=True, nullable=False)

    discount_type = Column(String(20))   
    discount_value = Column(Float)

    min_amount = Column(Float, nullable=True)

    usage_limit = Column(Integer, nullable=True)
    used_count = Column(Integer, default=0)
    
    is_first_time_only = Column(Boolean, default=False)

    is_active = Column(Boolean, default=True)

    expiry_date = Column(DateTime, nullable=True)
    coupon_type = Column(String, default="NORMAL")

    created_at = Column(DateTime, default=datetime.utcnow)