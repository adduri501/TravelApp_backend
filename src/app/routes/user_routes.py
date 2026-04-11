from fastapi import APIRouter, Depends, Path
import uuid
from app.services import user_service
from app.services.unit_of_work import UnitOfWork
from sqlalchemy.ext.asyncio import AsyncSession
from app.common.db_config import get_db
import json
from app.schemas.user_schema import UserUpdateSchema
from uuid import UUID, uuid4
# from app.common.auth import get_current_user

user_routes = APIRouter(prefix="/api", tags=["auth routes"])


@user_routes.get(
    "/user_info/{user_id}", description="Get user information by passing user id"
)
async def fetch_user_info(user_id: uuid.UUID, session: AsyncSession = Depends(get_db)):

    response = await user_service.fetch_user(
        user_id=user_id, unit_of_work=UnitOfWork(session=session)
    )
    return response


@user_routes.put(
    "/user_info/update/{user_id}",
    description="Update user information by passing user id",
)
async def update_user_info(
    user_id: UUID = Path(
        examples=[str(uuid4())],
        description="The unique identifier for the metadata.",
    ),
    # user=Depends(get_current_user),
    data=UserUpdateSchema,
    session: AsyncSession = Depends(get_db),
):

    data_to_update = json.loads(data)

    response = await user_service.update_user(
        user_id=user_id,
        update_data=data_to_update,
        unit_of_work=UnitOfWork(session=session),
    )
    return response
