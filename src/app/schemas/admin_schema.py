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


async def create_coupon(current_user, request, unit_of_work):
    async with unit_of_work as uow:

        if current_user.get("role") not in ["admin", "super_admin"]:
            raise Exception("Only admin can create coupons")

        existing = await uow.coupon_repo.get_by_code(request.code)
        if existing:
            raise Exception("Coupon already exists")

        coupon = await uow.coupon_repo.create({
            "code": request.code.upper(),
            "discount_type": request.discount_type,
            "discount_value": request.discount_value,
            "min_amount": request.min_amount,
            "usage_limit": request.usage_limit,
            "expiry_date": request.expiry_date,
        })

        await uow.commit()

        return {
            "message": "Coupon created",
            "coupon_id": coupon.id
        }

