from app.repositories.base_repository import BaseRepository
from app.orm.models.refresh_token_model import RefreshTokenTable
from app.entities.refresh_token_entity import RefreshTokenEntity
from app.common import utils
from sqlalchemy import or_, select


class RefreshTokenRepo(BaseRepository[RefreshTokenTable]):
    def __init__(self, session):
        self.model = RefreshTokenTable
        self.entity = RefreshTokenEntity
        super().__init__(RefreshTokenTable, session=session)

    def add(
        self,
    ):
        pass

    async def get_many(self):
        pass

    async def get_one(self, token_id):
        stmt = select(self.model).where(self.model.token_jti == token_id)
        result = await self.session.execute(stmt)
        user = result.scalars().first()
        return user

    async def save_refresh_token(self, entity_obj):
        db_obj = utils.entity_to_model(entity_obj, RefreshTokenTable)
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return utils.model_to_entity(db_obj, RefreshTokenEntity)

    async def revoke_token(self, token_jti: str):
        token = await self.get_one(token_jti)
        if not token:
            raise Exception("Token not found")
        token.is_revoked = True
