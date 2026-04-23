from fastapi import APIRouter,Depends,Query
from app.common.auth import get_current_user
from app.services import admin_service
from sqlalchemy.ext.asyncio import AsyncSession
from app.common.db_config import get_db
from app.services.admin_service import view_all_drivers as view_all_drivers_service
from app.schemas.admin_schema import CreateDriverRequest
from app.services.unit_of_work import UnitOfWork
from app.services import trip_service
from app.services.admin_service import *
from app.schemas.coupon_schema import*


admin_route = APIRouter(prefix="/api", tags=["admin routes"])


@admin_route.post("/admin/create-driver")
async def create_driver(
    request: CreateDriverRequest,
    current_user = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),

):
    return await admin_service.create_driver(
        current_user, request, unit_of_work=UnitOfWork(session=session)
    )



@admin_route.get("/admin/passengers")
async def all_passengers(
    current_user = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),

):
    return await admin_service.view_all_passengers(
        current_user, unit_of_work=UnitOfWork(session=session)
    )





@admin_route.get("/admin/drivers")
async def view_all_drivers(
    current_user = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    return await view_all_drivers_service(
        current_user,
        UnitOfWork(session=session)
    )

@admin_route.put("/admin/assign-driver/{trip_id}")
async def assign_driver_route(
    trip_id: str,
    driver_id: str = Query(...),
    current_user = Depends(get_current_user),  
    session: AsyncSession = Depends(get_db),
):
    return await trip_service.assign_driver(
        trip_id,
        driver_id,
        current_user,   
        UnitOfWork(session=session)
    )
    
@admin_route.post("/admin/create-coupon")
async def create_coupon_route(
    request: CreateCouponRequest,
    current_user = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    return await admin_service.create_coupon(
        current_user,
        request,
        UnitOfWork(session=session)
    )
    
@admin_route.get("/admin/coupons")
async def get_all_coupons_route(
    current_user = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    return await admin_service.get_all_coupons(
        current_user,
        UnitOfWork(session=session)
    )