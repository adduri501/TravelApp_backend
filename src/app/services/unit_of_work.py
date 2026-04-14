import abc
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user_repository import UserRepository
from app.repositories.otp_repository import OtpRepository
from app.repositories.device_repository import DeviceRepository
from app.repositories.refresh_token_repository import RefreshTokenRepo
from app.repositories.passenger_repository import PassengerRepository
from app.repositories.driver_repository import DriverRepository
from app.repositories.vehicle_repository import VehicleRepository


class BaseUnitOfWork(abc.ABC):
    async def __aenter__(self):
        return self

    async def __aexit__(self, *args, **kwargs):
        await self.rollback()

    @abc.abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def rollback(self):
        raise NotImplementedError


class UnitOfWork(BaseUnitOfWork):
    """
    Unified Unit of Work implementation for managing transactions
    across Message and Thread metadata operations.

    This implementation ensures that all database operations via the
    injected repositories are committed or rolled back atomically.

    Attributes:
        session (AsyncSession): The async DB session.
    """

    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repo = UserRepository(self.session)
        self.otp_repo = OtpRepository(self.session)
        self.device_repo = DeviceRepository(self.session)
        self.refresh_token = RefreshTokenRepo(self.session)
        self.passenger_repo = PassengerRepository(self.session)
        self.driver_repo = DriverRepository(self.session)
        self.vehicle_repo = VehicleRepository(self.session)

    async def __aenter__(self):
        return await super().__aenter__()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.rollback()
        else:
            await self.commit()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
