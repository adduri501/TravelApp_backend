
from fastapi import APIRouter,Depends

from app.common.auth import get_current_user
from app.services import admin_service
from sqlalchemy.ext.asyncio import AsyncSession
from app.common.db_config import get_db

from app.schemas.admin_schema import CreateDriverRequest
from app.services.unit_of_work import UnitOfWork


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
    return await admin_service.view_all_drivers(
        current_user, unit_of_work=UnitOfWork(session=session)
    )


