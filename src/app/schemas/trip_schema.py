# app/schemas/trip_schema.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date


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