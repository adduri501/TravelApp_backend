from sqlalchemy import select
from app.repositories.base_repository import BaseRepository
from app.orm.models.trip_model import TripTable
from app.orm.models.driver_model import DriverTable
from app.entities.trip_entity import TripEntity
from app.common import utils
from sqlalchemy.orm import selectinload
from app.orm.models.vehicle_model import VehicleTable


class TripRepository(BaseRepository):

    def __init__(self, session):
        self.model = TripTable
        self.entity = TripEntity
        super().__init__(TripTable, session=session)
        
    async def get_one_db(self, trip_id):
        stmt = select(TripTable).where(TripTable.id == trip_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def create(self, entity: TripEntity):
        obj = utils.entity_to_model(entity, TripTable)
        self.session.add(obj)
        await self.session.flush()
        return utils.model_to_entity(obj, TripEntity)

    async def add(self, entity: TripEntity):
        return await self.create(entity)

    async def get_many(self):
        stmt = select(self.model).options(selectinload(self.model.vehicle))
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update(self, db_obj, obj_in: dict):
        for key, value in obj_in.items():
            if hasattr(db_obj, key):
                setattr(db_obj, key, value)

        await self.session.flush()
        await self.session.refresh(db_obj)
        return utils.model_to_entity(db_obj, TripEntity)

    async def delete(self, db_obj):
        await self.session.delete(db_obj)
        await self.session.flush()
 
    async def get_one(self, trip_id):
        stmt = (
            select(
                TripTable,
                DriverTable.name,
                VehicleTable.vehicle_name,
                VehicleTable.color
                
            )
            .join(
                VehicleTable,
                TripTable.vehicle_number == VehicleTable.vehicle_number
                
            )
            .join(
            DriverTable,
            TripTable.driver_id == DriverTable.id,
            isouter=True   
            )
            .where(TripTable.id == trip_id)
        )

        result = await self.session.execute(stmt)
        row = result.first()

        if not row:
            return None

        trip, vehicle_name, driver_name,color = row

        return {
            "id": str(trip.id),
            "name": trip.name,
            "vehicle_number": trip.vehicle_number,
            "vehicle_name": vehicle_name,
            "color": color,
            "driver_name": driver_name, 
            "starting_date": trip.starting_date,
            "starting_time": trip.starting_time,
            "available_seats": trip.available_seats,
            "amount": trip.amount,
            "from": trip.from_location,
            "to": trip.to_location,
        }

    async def search_trips(
    self,
    starting_date=None,
    from_location=None,
    to_location=None,
    seats=None,
):
        stmt = (
            select(
            TripTable,
            DriverTable.name.label("driver_name"),
            VehicleTable.vehicle_name
        )
        .join(
            VehicleTable,
            TripTable.vehicle_number == VehicleTable.vehicle_number
        )
        .join(
            DriverTable,
            TripTable.driver_id == DriverTable.id,
            isouter=True   
        )
        )
    
        
        if starting_date:
            print("search api ",starting_date)
            print("search api ",from_location)
            print("search api ",to_location)
            stmt = stmt.where(TripTable.starting_date == starting_date)

        if from_location:
            print("search api ",from_location)
            stmt = stmt.where(
                TripTable.from_location.ilike(f"%{from_location.strip()}%")
            )

        if to_location:
            print("search api ",to_location)
            stmt = stmt.where(
                TripTable.to_location.ilike(f"%{to_location.strip()}%")
            )

        if seats:
            stmt = stmt.where(TripTable.available_seats >= seats)

        result = await self.session.execute(stmt)
        rows = result.all()
        trips = result.scalars().all()

        return [
            {
            "id": str(trip.id),
            "name": trip.name,
            "vehicle_number": trip.vehicle_number,
            "vehicle_name": vehicle_name,
            "driver_name": driver_name,   
            "starting_date": trip.starting_date,
            "starting_time": trip.starting_time,
            "available_seats": trip.available_seats,
            "amount": trip.amount,
            "from_location": trip.from_location,
            "to_location": trip.to_location,
        }
        for trip, driver_name, vehicle_name in rows
    ]
    async def get_trip_for_update(self, trip_id):
        stmt = (
            select(TripTable)
            .where(TripTable.id == trip_id)
            .with_for_update() 
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_by_id(self, trip_id):
        stmt = select(self.model).where(self.model.id == trip_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()