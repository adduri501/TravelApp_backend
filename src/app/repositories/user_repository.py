from app.repositories.base_repository import BaseRepository
import abc
from app.orm.models.user_model import UserTable
from app.entities.user_entity import UserEntity
from typing import Optional
from sqlalchemy import or_, select
from app.common import utils


class UserRepository(BaseRepository[UserTable]):
    def __init__(self, session):
        self.model = UserTable
        self.entity = UserEntity
        super().__init__(UserTable, session=session)

    async def add_user(self, obj: UserEntity):
        db_obj = utils.entity_to_model(entity=obj, model_class=UserTable)
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return utils.model_to_entity(db_obj, UserEntity)

    async def get_many(self):
        stmt = select(self.model)
        result = await self.session.execute(stmt)
        objs = result.scalars().all()
        return objs

    async def get_one(self, mobile_number):
        stmt = select(self.model).where(self.model.mobile_number == mobile_number)
        result = await self.session.execute(stmt)
        user = result.scalars().first()
        # user = utils.model_to_entity(user, UserEntity)
        return user

    async def get_one_by_user_id(self, user_id):
        stmt = select(self.model).where(self.model.id == user_id)
        result = await self.session.execute(stmt)
        user = result.scalars().first()
        # user = utils.model_to_entity(user, UserEntity)
        return user

    def add(
        self,
    ):
        pass

    async def update(self, db_obj: UserTable, obj_in: dict) -> UserEntity:
        valid_columns = self.model.__table__.columns.keys()
        for key, value in obj_in.items():
            if key in valid_columns:
                setattr(db_obj, key, value)
        await self.session.flush()
        await self.session.refresh(db_obj)
        return utils.model_to_entity(db_obj, UserEntity)
    
    async def get_by_username(self, username):
        print(username,58585858858585588585858)
        # query DB where username = given

        stmt = select(self.model).where(self.model.username == username)
        print(stmt,662662626262626262626266266262)
        result = await self.session.execute(stmt)
        user = result.scalars().first()
        # user = utils.model_to_entity(user, UserEntity)
        print(user,6565566656565656656565656)
        return user
        pass

    # async def create(self, user_data: dict):
    #     # insert into DB
    #     pass
