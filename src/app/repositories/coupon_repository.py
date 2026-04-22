from sqlalchemy import select
from app.orm.models.coupon_model import CouponTable

class CouponRepository:
    def __init__(self, session):
        self.session = session

    async def create(self, data):
        obj = CouponTable(**data)
        self.session.add(obj)
        await self.session.flush()
        return obj

    async def get_by_code(self, code):
        stmt = select(CouponTable).where(CouponTable.code == code)
        result = await self.session.execute(stmt)
        return result.scalars().first()
    
    async def get_all(self):
        stmt = select(CouponTable)
        result = await self.session.execute(stmt)
        return result.scalars().all()