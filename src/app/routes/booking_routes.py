from fastapi import APIRouter, Depends ,Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.booking_schema import BookTripRequest
from app.services.booking_service import book_trip
from app.common.auth import get_current_user
from app.common.db_config import get_db
from app.services.unit_of_work import UnitOfWork
from app.schemas.booking_schema import *
from app.services import booking_service
from app.services.booking_service import get_my_bookings
from app.services.booking_service import cancel_booking

booking_route = APIRouter(prefix="/api", tags=["Booking"])

@booking_route.post("/apply-coupon")
async def apply_coupon_route(
    request: ApplyCouponRequest,
    session: AsyncSession = Depends(get_db),
):
    return await booking_service.apply_coupon(
        request,
        UnitOfWork(session=session)
    )
    
@booking_route.post("/book-trip")
async def book_trip_route(
    request: BookTripRequest,
    applied_coupon_code: str = Query(None),   # 👈 NEW PARAM
    current_user = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    return await booking_service.book_trip(
        request,
        applied_coupon_code,   # 👈 pass it
        current_user,
        UnitOfWork(session=session)
    )

@booking_route.get("/my-bookings")
async def my_bookings(
    current_user = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    return await get_my_bookings(
        current_user,
        UnitOfWork(session=session)
    )
    
@booking_route.put("/cancel-booking/{booking_id}")
async def cancel_booking_route(
    booking_id: str,
    current_user = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    return await cancel_booking(
        booking_id,
        current_user,
        UnitOfWork(session=session)
    )