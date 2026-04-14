from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.trip_schema import CreateTripRequest, UpdateTripRequest
from app.services import trip_service
from app.services.unit_of_work import UnitOfWork
from app.common.db_config import get_db


trip_route = APIRouter(prefix="/api", tags=["Trip"])


@trip_route.post("/admin/create-trip")
async def create_trip(
    request: CreateTripRequest,
    session: AsyncSession = Depends(get_db),
):
    return await trip_service.create_trip(
        request,
        UnitOfWork(session=session),
    )
    
@trip_route.get("/admin/trips")
async def get_all_trips(
    session: AsyncSession = Depends(get_db),
):
    return await trip_service.get_all_trips(
        UnitOfWork(session=session),
    )
@trip_route.get("/admin/trips/{trip_id}")
async def get_trip_by_id(
    trip_id: str,
    session: AsyncSession = Depends(get_db),
):
    return await trip_service.get_trip_by_id(
        trip_id,
        UnitOfWork(session=session),
    )

@trip_route.put("/admin/update-trip/{trip_id}")
async def update_trip(
    trip_id: str,
    request: UpdateTripRequest,
    session: AsyncSession = Depends(get_db),
):
    return await trip_service.update_trip(
        trip_id,
        request,
        UnitOfWork(session=session),
    )


@trip_route.delete("/admin/delete-trip/{trip_id}")
async def delete_trip(
    trip_id: str,
    session: AsyncSession = Depends(get_db),
):
    return await trip_service.delete_trip(
        trip_id,
        UnitOfWork(session=session),
    )


