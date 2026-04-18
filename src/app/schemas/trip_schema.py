# app/schemas/trip_schema.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date


from enum import Enum


class TripStatus(str, Enum):
    SCHEDULED = "scheduled"
    STARTED = "started"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class TripBase(BaseModel):
    name: str
    vehicle_number: str
    starting_date: date
    starting_time: datetime
    available_seats: int
    amount: float
    from_location: Optional[str] = None
    to_location: Optional[str] = None
    driver_id: Optional[str] = None
    status: Optional[TripStatus] = "not started"


class CreateTripRequest(TripBase):
    pass


class UpdateTripRequest(BaseModel):
    name: Optional[str] = None
    vehicle_number: Optional[str] = None
    starting_date: Optional[date] = None
    starting_time: Optional[datetime] = None
    available_seats: Optional[int] = None
    amount: Optional[float] = None
    from_location: Optional[str] = None
    to_location: Optional[str] = None


class UpdateStatusDriverSchema(BaseModel):
    status: TripStatus
