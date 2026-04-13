from app.entities.otp_entity import OtpEntity
from app.repositories.base_repository import BaseRepository
from app.orm.models.otp_model import OtpTable
from sqlalchemy import or_, select, and_
from app.common import utils


class OtpRepository(BaseRepository[OtpTable]):
    def __init__(self, session):
        self.model = OtpTable
        self.entity = OtpEntity
        super().__init__(OtpTable, session=session)

    async def add(
        self,
    ):
        pass

    async def get_many(self, limit, offset):
        return super().get_many(limit, offset)

    async def get_one(self, mobile_number, otp_code):
        stmt = select(self.model).where(
            and_(self.model.mobile_number == mobile_number, self.model.otp == otp_code)
        )
        result = await self.session.execute(stmt)
        otp_obj = result.scalars().first()
        # otp_obj= utils.model_to_entity(otp_obj, self.entity)
        return otp_obj

    async def save_otp(self, obj: OtpEntity):
        db_obj = utils.entity_to_model(entity=obj, model_class=OtpTable)
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return utils.model_to_entity(db_obj, OtpEntity)

    async def update(self, db_obj: OtpTable, obj_in):
        valid_columns = self.model.__table__.columns.keys()
        for key, value in obj_in.items():
            if key in valid_columns:
                setattr(db_obj, key, value)
        await self.session.flush()
        await self.session.refresh(db_obj)
        return db_obj

        # return utils.model_to_entity(db_obj,OtpTable)
