from fastapi import APIRouter, Depends,Body
from app.common.auth import get_current_user
from app.common.db_config import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.admin_schema import CreateAdminRequest, CreateDriverRequest
from app.services import admin_service
from app.services.unit_of_work import UnitOfWork


super_admin_route = APIRouter(prefix="/api", tags=["admin routes"])


@super_admin_route.post("/admin/create-admin")
async def create_admin(
    request: CreateAdminRequest,
    current_user=Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    

    return await admin_service.create_admin(
        current_user, request, unit_of_work=UnitOfWork(session=session)
    )

