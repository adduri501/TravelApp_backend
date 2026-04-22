from sqlalchemy import select
from app.orm.models.booking_model import BookingTable

class BookingRepository:

    def __init__(self, session):
        self.session = session

    async def create(self, data: dict):
        booking = BookingTable(**data)
        self.session.add(booking)
        await self.session.flush()
        return booking

    async def get_by_user(self, user_id):
        stmt = select(BookingTable).where(BookingTable.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_id(self, booking_id):
        stmt = select(BookingTable).where(BookingTable.id == booking_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()