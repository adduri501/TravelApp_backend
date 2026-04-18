from app.entities.trip_entity import TripEntity
from app.common.exceptions import NotFoundException, AppException


async def create_trip(req, unit_of_work, current_user):
    async with unit_of_work as uow:
        if current_user.get("role") != "admin":
            raise AppException(detail="Only super admin can create admin")
        trip = TripEntity(
            name=req.name,
            vehicle_number=req.vehicle_number,
            starting_date=req.starting_date,
            starting_time=req.starting_time,
            available_seats=req.available_seats,
            amount=req.amount,
            from_location=req.from_location,
            to_location=req.to_location,
            driver_id=req.driver_id,
        )

        result = await uow.trip_repo.create(trip)
        await uow.commit()
        return result


async def update_trip(trip_id, req, unit_of_work, current_user):
    async with unit_of_work as uow:
        if current_user.get("role") != "admin":
            raise AppException(detail="Only super admin can create admin")

        trip = await uow.trip_repo.get_one_db(trip_id)
        if not trip:
            raise NotFoundException("Trip not found")

        updated = await uow.trip_repo.update(trip, req.dict(exclude_unset=True))

        await uow.commit()
        return updated


async def delete_trip(trip_id, unit_of_work, current_user):
    async with unit_of_work as uow:
        if current_user.get("role") != "admin":
            raise AppException(detail="Only super admin can create admin")

        trip = await uow.trip_repo.get_one_db(trip_id)
        if not trip:
            raise NotFoundException("Trip not found")

        await uow.trip_repo.delete(trip)
        await uow.commit()

        return {"message": "Trip deleted successfully"}


async def get_all_trips(unit_of_work, current_user):
    async with unit_of_work as uow:
        if current_user.get("role") != "admin":
            raise AppException(detail="Only super admin can create admin")
        return await uow.trip_repo.get_many()


async def get_trip_by_id(trip_id, unit_of_work, current_user):
    async with unit_of_work as uow:
        if current_user.get("role") != "admin":
            raise AppException(detail="Only super admin can create admin")

        trip = await uow.trip_repo.get_one(trip_id)

        if not trip:
            raise Exception("Trip not found")

        return trip


async def search_trips(
    starting_date, from_location, to_location, seats, unit_of_work, current_user
):
    async with unit_of_work as uow:
        if current_user.get("role") != "admin":
            raise AppException(detail="Only super admin can create admin")

        trips = await uow.trip_repo.search_trips(
            starting_date, from_location, to_location, seats
        )

        return trips


async def assign_driver(trip_id, driver_id, unit_of_work, current_user):
    async with unit_of_work as uow:
        if current_user.get("role") != "admin":
            raise AppException(detail="Only super admin can create admin")

        # check trip exists
        trip = await uow.trip_repo.get_one_db(trip_id)
        if not trip:
            raise Exception("Trip not found")

        # check driver exists
        driver = await uow.driver_repo.get_by_id(driver_id)
        if not driver:
            raise Exception("Driver not found")

        # ✅ directly update field (same session)
        trip.driver_id = driver_id

        await uow.commit()

        return {
            "message": "Driver assigned successfully",
            "trip_id": trip_id,
            "driver_id": driver_id,
        }


async def update_status_of_trip(
    trip_id,
    # current_user,
    req_body,
    unit_of_work,
):
    async with unit_of_work as uow:
        trip = await uow.trip_repo.get_one_db(trip_id)
        # check trip exists
        if not trip:
            raise Exception("Trip not found")
        # if current_user.role == "driver":
        # check driver exists
        driver = await uow.driver_repo.get_by_id(trip.driver_id)

        if not driver:
            raise NotFoundException("Trips is not assigned to this particular Driver")

        trip.status = req_body.status
        # ✅ directly update field (same session)
        await uow.commit()

        return {
            "message": "Driver updated status successfully",
            "trip_id": trip_id,
        }
