from app.entities.passenger_entity import PassengerEntity
from app.services.unit_of_work import UnitOfWork
from fastapi import HTTPException, status


async def create_passenger(req_body, unit_of_work: UnitOfWork):
    async with unit_of_work as uow:
        print(req_body,56565665665656565656565)

        existing = await uow.passenger_repo.get_passenger_by_user_id(req_body.user_id)
        if existing:
            raise HTTPException(
                detail="Passenger already exists", status_code=status.HTTP_302_FOUND
            )
        passenger_entity = PassengerEntity(
            user_id=req_body.user_id, name=req_body.name, email=req_body.email
        )
        result_obj = await unit_of_work.passenger_repo.create(passenger_entity)
        await unit_of_work.commit()
        return result_obj


async def fetch_passenger(user_id: str, unit_of_work: UnitOfWork):
    async with unit_of_work as uow:
        existing = await uow.passenger_repo.get_passenger_by_user_id(user_id)

        if not existing:
            raise HTTPException(
                detail="Passenger not found with this user",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        return {
                "user": existing.__dict__ if existing else None,
                "messages": (
                    "Passenger retrieved successfully."
                    if existing
                    else "Passenger not found!"
                ),
            }



async def update_passenger(user_id, data_to_update, unit_of_work: UnitOfWork):
    print(user_id,data_to_update,454554545454544554544554545)
    async with unit_of_work as uow:
        existing_passenger = await uow.passenger_repo.get_passenger_by_user_id(user_id)
        if existing_passenger:

            updated_passenger = await uow.passenger_repo.update(
                db_obj=existing_passenger, obj_in=data_to_update
            )

            return {
                "data": {
                    "user_name": updated_passenger.get("name"),
                    "user_id": updated_passenger.get("id"),
                },
                "message": "Passenger updated successfully",
            }
        return HTTPException(
            detail="Passenger not found with this user",
            status_code=status.HTTP_404_NOT_FOUND,
        )
