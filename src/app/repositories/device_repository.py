from app.repositories.base_repository import BaseRepository
from app.orm.models.device_model import DeviceTable
from app.entities.user_device_entity import UserDeviceEntity
from app.common import utils
from sqlalchemy import or_, select


class DeviceRepository(BaseRepository[DeviceTable]):

    def __init__(self, session):
        self.model = DeviceTable
        self.entity = UserDeviceEntity
        super().__init__(DeviceTable, session=session)

    async def create(self, obj: UserDeviceEntity):
        db_obj = utils.entity_to_model(entity=obj, model_class=DeviceTable)
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def get_device(self, device_token):
        stmt = select(self.model).where(self.model.device_token == device_token)
        result = await self.session.execute(stmt)
        device = result.scalars().first()
        if device is None:
            return None
        else:
            user = utils.model_to_entity(DeviceTable, UserDeviceEntity)
            return user

    async def add(self):
        pass

    async def get_one(self):
        pass

    async def get_many(self):
        pass
