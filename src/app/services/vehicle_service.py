from app.entities.vehicle_entity import VehicleEntity
from app.common.exceptions import ConflictException, NotFoundException


async def add_vehicle(req, unit_of_work):
    async with unit_of_work as uow:

        existing = await uow.vehicle_repo.get_by_vehicle_number(req.vehicle_number)
        if existing:
            raise ConflictException("Vehicle already exists")

        vehicle = VehicleEntity(
            vehicle_number=req.vehicle_number,
            vehicle_name=req.vehicle_name,
             color=req.color,             
             no_of_seats=req.no_of_seats, 
        )

        result = await uow.vehicle_repo.create(vehicle)
        await uow.commit()
        return result


async def update_vehicle(vehicle_id, req, unit_of_work):
    async with unit_of_work as uow:

        vehicle = await uow.vehicle_repo.get_one(vehicle_id)
        if not vehicle:
            raise NotFoundException("Vehicle not found")

        updated = await uow.vehicle_repo.update(
            vehicle,
            req.dict(exclude_unset=True)
        )

        await uow.commit() 

        return updated

        print("Incoming update:", req.dict(exclude_unset=True))


async def delete_vehicle(vehicle_id, unit_of_work):
    async with unit_of_work as uow:

        vehicle = await uow.vehicle_repo.get_one(vehicle_id)
        if not vehicle:
            raise NotFoundException("Vehicle not found")

        await uow.vehicle_repo.delete(vehicle)
        await uow.commit()

        return {"message": "Vehicle deleted successfully"}


async def get_all_vehicles(unit_of_work):
    async with unit_of_work as uow:
        vehicles = await uow.vehicle_repo.get_many()
        return vehicles


async def get_vehicle_by_id(vehicle_id, unit_of_work):
    async with unit_of_work as uow:

        vehicle = await uow.vehicle_repo.get_one(vehicle_id)
        if not vehicle:
            raise NotFoundException("Vehicle not found")

        return vehicle