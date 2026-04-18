from sqlalchemy import select
from app.repositories.base_repository import BaseRepository
from app.orm.models.vehicle_model import VehicleTable
from app.entities.vehicle_entity import VehicleEntity
from app.common import utils
from datetime import datetime


class VehicleRepository(BaseRepository):
    def __init__(self, session):
        self.model = VehicleTable
        self.entity = VehicleEntity
        super().__init__(VehicleTable, session=session)

    async def create(self, entity: VehicleEntity):
        db_obj = utils.entity_to_model(entity=entity, model_class=VehicleTable)
        self.session.add(db_obj)
        await self.session.flush()
        return utils.model_to_entity(db_obj, VehicleEntity)

    async def add(self, entity: VehicleEntity):
        return await self.create(entity)


    async def get_one(self, vehicle_id):
        stmt = select(self.model).where(self.model.id == vehicle_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()

  
    async def get_many(self):
        stmt = select(self.model)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    
    async def get_by_vehicle_number(self, vehicle_number: str):
        stmt = select(self.model).where(
            self.model.vehicle_number == vehicle_number
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    
    async def update(self, db_obj: VehicleTable, obj_in: dict):
        valid_columns = self.model.__table__.columns.keys()

        for key, value in obj_in.items():
            if key in valid_columns:
                setattr(db_obj, key, value)

    
        db_obj.updated_at = datetime.utcnow()

        await self.session.flush()
        await self.session.refresh(db_obj)

        return utils.model_to_entity(db_obj, VehicleEntity)
    
    async def delete(self, db_obj: VehicleTable):
        await self.session.delete(db_obj)
        await self.session.flush()