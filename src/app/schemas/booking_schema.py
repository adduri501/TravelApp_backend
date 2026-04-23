from pydantic import BaseModel
from typing import Optional


class ApplyCouponRequest(BaseModel):
    trip_id: str
    seats: int
    coupon_code: str


class BookTripRequest(BaseModel):
    trip_id: str
    seats: int
    applied_coupon_code: Optional[str] = None
    transaction_id: Optional[str] = None