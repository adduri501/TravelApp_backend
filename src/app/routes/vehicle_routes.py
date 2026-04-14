# app/routes/vehicle_routes.py

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.vehicle_schema import CreateVehicleRequest, UpdateVehicleRequest
from app.services import vehicle_service
from app.services.unit_of_work import UnitOfWork
from app.common.db_config import get_db
from fastapi import Body


vehicle_route = APIRouter(prefix="/api", tags=["vehicle routes"])


@vehicle_route.post("/admin/add-vehicle")
async def add_vehicle(
    request: CreateVehicleRequest,
    session: AsyncSession = Depends(get_db),
):
    return await vehicle_service.add_vehicle(
        request,
        UnitOfWork(session=session),
    )


@vehicle_route.put("/admin/update-vehicle/{vehicle_id}")
async def update_vehicle(
    vehicle_id: str,
    request: UpdateVehicleRequest=Body(...),
    session: AsyncSession = Depends(get_db),
):
    return await vehicle_service.update_vehicle(
        vehicle_id,
        request,
        UnitOfWork(session=session),
    )


@vehicle_route.delete("/admin/delete-vehicle/{vehicle_id}")
async def delete_vehicle(
    vehicle_id: str,
    session: AsyncSession = Depends(get_db),
):
    return await vehicle_service.delete_vehicle(
        vehicle_id,
        UnitOfWork(session=session),
    )


@vehicle_route.get("/admin/all-vehicles")
async def get_all_vehicles(
    session: AsyncSession = Depends(get_db),
):
    return await vehicle_service.get_all_vehicles(
        UnitOfWork(session=session),
    )


@vehicle_route.get("/admin/{vehicle_id}")
async def get_vehicle(
    vehicle_id: str,
    session: AsyncSession = Depends(get_db),
):
    return await vehicle_service.get_vehicle_by_id(
        vehicle_id,
        UnitOfWork(session=session),
    )