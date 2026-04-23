from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CreateCouponRequest(BaseModel):
    code: str
    discount_type: str   
    discount_value: float
    min_amount: Optional[float] = None
    usage_limit: Optional[int] = None
    expiry_date: Optional[datetime] = None