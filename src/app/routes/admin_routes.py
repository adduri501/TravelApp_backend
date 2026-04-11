
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
    print(current_user,32322332233232322323322332)
    return await admin_service.create_driver(
        current_user, request, unit_of_work=UnitOfWork(session=session)
    )




