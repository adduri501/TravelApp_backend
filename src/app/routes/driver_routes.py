from fastapi import APIRouter, Depends, Path
from app.services import driver_service
from app.schemas.driver_schema import CreateDriverRequest, UpdateDriverRequest
from app.common.db_config import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.unit_of_work import UnitOfWork


driver_route = APIRouter(prefix="/api", tags=["Driver routes"])


@driver_route.post("/driver/profile")
async def create_driver(
    req_body: CreateDriverRequest, session: AsyncSession = Depends(get_db)
):

    response = await driver_service.create_driver(
        req_body, unit_of_work=UnitOfWork(session=session)
    )
    return response


@driver_route.get("/driver/profile")
async def fetch_driver():
    pass


@driver_route.put("/driver/profile")
async def update_driver(
    data: UpdateDriverRequest, session: AsyncSession = Depends(get_db)
):
    await driver_service.update_driver(data, unit_of_work=UnitOfWork(session=session))


@driver_route.patch("/driver/profile")
async def partially_update_driver():
    pass


@driver_route.patch("/driver/verify")
async def verify_driver():
    pass
