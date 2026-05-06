from sqlalchemy import select , func
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
    
    async def has_used_coupon(self, user_id, coupon_code):
        stmt = select(BookingTable.id).where(
            BookingTable.user_id == user_id,
            BookingTable.coupon_code == coupon_code,
            BookingTable.status != "cancelled"
        ).limit(1)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None

   
    async def count_user_successful_bookings(self, user_id):
        stmt = (
            select(func.count())
            .select_from(BookingTable)
            .where(
                BookingTable.user_id == user_id,
                func.lower(BookingTable.status) == "booked"
            )
        )

        result = await self.session.execute(stmt)
        return result.scalar_one()