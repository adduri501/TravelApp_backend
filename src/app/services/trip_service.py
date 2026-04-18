from app.entities.trip_entity import TripEntity
from app.common.exceptions import NotFoundException


async def create_trip(req, unit_of_work):
    async with unit_of_work as uow:

        trip = TripEntity(
            name=req.name,
            vehicle_number=req.vehicle_number,
            starting_date=req.starting_date,
            starting_time=req.starting_time,
            available_seats=req.available_seats,
            amount=req.amount,
            from_location=req.from_location,
            to_location=req.to_location,
        )

        result = await uow.trip_repo.create(trip)
        await uow.commit()
        return result


async def update_trip(trip_id, req, unit_of_work):
    async with unit_of_work as uow:

        trip = await uow.trip_repo.get_one(trip_id)
        if not trip:
            raise NotFoundException("Trip not found")

        updated = await uow.trip_repo.update(
            trip,
            req.dict(exclude_unset=True)
        )

        await uow.commit()
        return updated


async def delete_trip(trip_id, unit_of_work):
    async with unit_of_work as uow:

        trip = await uow.trip_repo.get_one(trip_id)
        if not trip:
            raise NotFoundException("Trip not found")

        await uow.trip_repo.delete(trip)
        await uow.commit()

        return {"message": "Trip deleted successfully"}


async def get_all_trips(unit_of_work):
    async with unit_of_work as uow:
        return await uow.trip_repo.get_many()
    
async def get_trip_by_id(trip_id, unit_of_work):
    async with unit_of_work as uow:

        trip = await uow.trip_repo.get_one(trip_id)

        if not trip:
            raise Exception("Trip not found")

        return trip   
async def search_trips(starting_date, from_location, to_location, seats, unit_of_work):
    async with unit_of_work as uow:

        trips = await uow.trip_repo.search_trips(
            starting_date,
            from_location,
            to_location,
            seats
        )

        return trips