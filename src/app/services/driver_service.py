from app.services.unit_of_work import UnitOfWork
from app.entities.driver_entity import DriverEntity
from fastapi import HTTPException, status
from app.common.exceptions import (
    BadRequestException,
    ConflictException,
    NotFoundException,
    ForbiddenException,
)


async def create_driver(user, req_body, unit_of_work: UnitOfWork):
    async with unit_of_work as uow:
        if user.role != "driver":
            raise Exception("User is not a driver")

        # 🔍 already exists
        existing = await uow.driver_repo.get_by_user_id(user.id)

        if existing:
            raise ConflictException("Driver profile already exists")
        # 🔥 uniqueness checks
        await _validate_uniqueness(uow, req_body)

        driver_entity = DriverEntity(
            user_id=user.id,
            name=req_body.name,
            license_number=req_body.license_number,
            vehicle_number=req_body.vehicle_number,
            address=req_body.address,
            aadhaar_number=req_body.aadhaar_number,
        )
        result = await uow.driver_repo.create(driver_entity)
        await uow.commit()
        return result


async def get_driver():
    pass


async def view_all_drivers(current_user, unit_of_work):
    print("SERVICE CALLED")  # 🔍 must print

    async with unit_of_work as uow:
        drivers = await uow.driver_repo.get_all_drivers()

        # ALWAYS return JSON (not ORM objects)
        return {
            "success": True,
            "data": [
                {
                    "id": str(d.id),
                    "name": d.name,
                    "license_number": d.license_number,
                    "aadhaar_number": d.aadhaar_number,
                    "is_verified": d.is_verified,
                    "address": d.address
                }
                for d in drivers
            ]
        }
        
async def update_driver(user, update_data: dict, unit_of_work: UnitOfWork):
    async with unit_of_work as uow:
        existing_driver = await uow.driver_repo.get_by_user_id(user.id)
        if not existing_driver:
            raise NotFoundException("Driver not found")

        await _validate_uniqueness(uow, update_data, exclude_user_id=user.id)
        updated_driver = await unit_of_work.driver_repo.update(
            db_obj=existing_driver, obj_in=update_data
        )
        await uow.commit()
        updated_driver_data = updated_driver.to_dict()
        return {
            "data": {
                "driver_name": updated_driver_data.get("name"),
                "driver_id": updated_driver_data.get("id"),
            },
            "message": "Driver updated successfully",
        }


async def partially_update_driver():
    pass


async def is_driver_verified(user_id, unit_of_work: UnitOfWork):
    async with unit_of_work as uow:

        driver = await uow.driver_repo.verify_driver(user_id)

        if not driver:
            raise NotFoundException("Driver not found")

        await uow.commit()

        return driver


async def _validate_uniqueness(uow, req, exclude_user_id=None):

    # Aadhaar check
    if req.aadhaar_number:
        existing = await uow.driver_repo.get_by_aadhaar(req.aadhaar_number)

        if existing and existing.user_id != exclude_user_id:
            raise ConflictException("Aadhaar already exists")

    # License check
    if req.license_number:
        existing = await uow.driver_repo.get_by_license(req.license_number)

        if existing and existing.user_id != exclude_user_id:
            raise ConflictException("License already exists")
        
