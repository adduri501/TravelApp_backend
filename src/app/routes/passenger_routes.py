from fastapi import APIRouter, Depends,Path
from app.services import passenger_service
from app.services.unit_of_work import UnitOfWork
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.passenger_schema import PassengerInputSchema, PassengerUpdateSchema
from app.common.db_config import get_db
import json

passenger_route = APIRouter(prefix="/api", tags=["Passenger routes"])


@passenger_route.post("/passenger/profile", description="Register passenger")
async def register_passenger(
    req_body: PassengerInputSchema, session: AsyncSession = Depends(get_db)
):
    print(161661661616166161661616161616)
    response = await passenger_service.create_passenger(
        req_body, unit_of_work=UnitOfWork(session=session)
    )
    return response


@passenger_route.get("/passenger/profile", description="Get passenger")
async def fetch_passenger(user_id: str, session: AsyncSession = Depends(get_db)):
    response = await passenger_service.fetch_passenger(
        user_id, unit_of_work=UnitOfWork(session=session)
    )
    return response
from uuid import UUID, uuid4

@passenger_route.put("/passenger/profile/{user_id}", description="Update passenger")
async def update_passenger(
     data: PassengerUpdateSchema,user_id: UUID = Path(
        examples=[str(uuid4())],
        description="The unique identifier for the metadata.",
    ), session: AsyncSession = Depends(get_db)
):  
    print(type(data))
    data_to_update = json.loads(data)
    response = passenger_service.update_passenger(
        user_id, data=data_to_update, unit_of_work=UnitOfWork(session=session)
    )

    return response
