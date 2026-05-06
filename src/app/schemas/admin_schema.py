from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CreateAdminRequest(BaseModel):
    username: str
    password: str
    name: Optional[str] = None
    role: Optional[str] = None


class CreateDriverRequest(BaseModel):
    mobile_number: str
    license_number: str
    aadhaar_number: str

    name: Optional[str] = None
    profile_pic: Optional[str] = None
    gender: Optional[str] = None
    dob: Optional[datetime] = None
    role: Optional[str] = None


class UpdateCouponRequest(BaseModel):
    code: Optional[str] = None
    discount_type: Optional[str] = None
    discount_value: Optional[float] = None
    min_amount: Optional[float] = None
    usage_limit: Optional[int] = None
    is_active: Optional[bool] = None
    is_first_time_only: Optional[bool] = None

