from app.repositories.base_repository import BaseRepository
from app.orm.models.passenger_model import PassengerTable
from app.entities.passenger_entity import PassengerEntity
from app.common import utils

from sqlalchemy import select


class PassengerRepository(BaseRepository[PassengerTable]):
    def __init__(self, session):
        self.model = PassengerTable
        self.entity = PassengerEntity
        super().__init__(PassengerTable, session=session)

    async def create(self, obj: PassengerEntity):
        db_obj = utils.entity_to_model(entity=obj, model_class=PassengerTable)
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def get_passenger_by_user_id(self, user_id):
        stmt = select(self.model).where(self.model.user_id == user_id)
        result = await self.session.execute(stmt)
        passenger = result.scalars().first()
        if passenger is None:
            return None
        else:
            # passenger = utils.model_to_entity(PassengerTable, PassengerEntity)
            return passenger

    async def update(self, db_obj: PassengerTable, obj_in: dict):
        valid_columns = self.model.__table__.columns.keys()
        for key, value in obj_in.items():
            if key in valid_columns:
                setattr(db_obj, key, value)
        await self.session.flush()
        await self.session.refresh(db_obj)
        return utils.model_to_entity(db_obj, PassengerEntity)

    async def add(self):
        pass

    async def get_one(self):
        pass

    async def get_many(self):
        pass
