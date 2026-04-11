from app.repositories.base_repository import BaseRepository

from app.orm.models.driver_model import DriverTable
from app.entities.driver_entity import DriverEntity
from app.common import utils
from sqlalchemy import or_, select


class DriverRepository(BaseRepository[DriverTable]):
    def __init__(self, session):
        self.model = DriverTable
        self.entity = DriverEntity
        super().__init__(DriverTable, session=session)

    async def create(self, entity: DriverEntity) -> DriverEntity:
        driver_db_obj = utils.entity_to_model(entity=DriverEntity, model=DriverTable)

        self.session.add(driver_db_obj)
        await self.session.flush()  # 🔥 get ID without commit

        return utils.model_to_entity(driver_db_obj, DriverEntity)

    async def get_by_user_id(self, user_id: str) -> DriverEntity | None:
        stmt = select(self.model).where(self.model.user_id == user_id)
        result = await self.session.execute(stmt)
        user = result.scalars().first()

        return user  # user object

    async def update(self, db_obj: DriverTable, obj_in: dict) -> DriverEntity | None:
        valid_columns = self.model.__table__.columns.keys()
        for key, value in obj_in.items():
            if key in valid_columns:
                setattr(db_obj, key, value)

        await self.session.flush()
        await self.session.refresh(db_obj)
        return utils.model_to_entity(db_obj, DriverEntity)

    async def verify_driver(self, user_id: str) -> DriverEntity | None:
        result = await self.session.execute(
            select(DriverTable).where(DriverTable.user_id == user_id)
        )
        driver = result.scalar_one_or_none()

        if not driver:
            return None

        driver.is_verified = True

        await self.session.flush()

        return self._to_entity(driver)

    async def get_by_aadhaar_or_licence_number(
        self, aadhaar_number: str = None, license_number: str = None
    ):
        stmt = select(self.model).where(
            or_(
                self.model.aadhaar_number == aadhaar_number,
                self.model.license_number == license_number,
            )
        )
        result = await self.session.execute(stmt)
        user = result.scalars().first()
        return user

    async def get_by_license(self, license_number: str):
        stmt = select(self.model).where(self.model.license_number == license_number)
        result = await self.session.execute(stmt)
        user = result.scalars().first()
        return user

    async def get_by_aadhaar(self, aadhaar_number: str = None):
        print(aadhaar_number,747747474747747477474)
        stmt = select(self.model).where(self.model.aadhaar_number == aadhaar_number)
        result = await self.session.execute(stmt)
        user = result.scalars().first()
        return user

    async def add(self):
        pass

    async def get_one(self):
        pass

    async def get_many(self):
        pass
