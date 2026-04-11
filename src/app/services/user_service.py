from app.services.unit_of_work import UnitOfWork
from app.entities.user_entity import UserEntity
from typing import Optional
from uuid import UUID
from app.common import utils


async def register_user(req_body: object, unit_of_work: UnitOfWork):
    async with unit_of_work as uow:
        user_obj = UserEntity(
            name=req_body.name,
            mobile_number=req_body.mobile_number,
            email=req_body.email,
            alternative_mobile_number=req_body.alternative_mobile_number,
            gender=req_body.gender,
        )
        result_obj = await unit_of_work.user_repo.add_user(user_obj)
        return {"message": "user created successfully", "data": {"id": user_obj.id}}


async def fetch_user(
    unit_of_work: UnitOfWork,
    user_id: Optional[UUID] = None,
):
    async with unit_of_work as uow:
        if user_id:
            existing_user = await unit_of_work.user_repo.get_one_by_user_id(
                user_id=user_id
            )
            return {
                "user": existing_user.__dict__ if existing_user else None,
                "messages": (
                    "User retrieved successfully."
                    if existing_user
                    else "User not found!"
                ),
            }


async def create_user(req_body, unit_of_work: UnitOfWork):
    async with unit_of_work as uow:
        user = await unit_of_work.user_repo.get_one(
            mobile_number=req_body.mobile_number
        )
        if user:
            return user, False
        user_entity_obj = UserEntity(
            mobile_number=req_body.mobile_number if req_body.mobile_number else None,
            role=req_body.role if hasattr(req_body, "role") else None,
            name=req_body.name if hasattr(req_body, "name") else None,
            email=req_body.email if hasattr(req_body, "email") else None,
            alternative_mobile_number=getattr(
                req_body, "alternative_mobile_number", None
            ),
            profile_pic=getattr(req_body, "profile_pic", None),
            gender=getattr(req_body, "gender", None),
        )
        user = await unit_of_work.user_repo.add_user(user_entity_obj)
        return user, True


async def update_user(user_id: UUID, update_data: dict, unit_of_work: UnitOfWork):
    """
    Update an existing user's details in the database.

    Args:
        user_id (UUID): The unique identifier of the agent to be updated.
        update_data (dict): A dictionary containing the fields to update and their new values.
        unit_of_work (UnitOfWork): The unit of work instance to manage database transactions.

    Returns:
        dict: A dictionary containing the updated agent's name and a success or failure message.
    """
    async with unit_of_work:
        existing_user = await unit_of_work.user_repo.get_one_by_user_id(user_id=user_id)
        if existing_user:
            updated_user = await unit_of_work.user_repo.update(
                db_obj=existing_user, obj_in=update_data
            )

            updated_user_data = updated_user.to_dict()

            return {
                "data": {
                    "user_name": updated_user_data.get("name"),
                    "user_id": updated_user_data.get("id"),
                },
                "message": "User updated successfully",
            }
        return {"data": None, "message": "User not found with this ID!"}
