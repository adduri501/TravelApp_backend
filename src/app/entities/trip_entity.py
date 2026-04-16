from typing import Optional
from datetime import datetime, date
import uuid


class TripEntity:
    def __init__(
        self,
        name: str,
        vehicle_number: str,
        starting_date: date,
        starting_time: datetime,
        available_seats: int,
        amount: float,
        from_location: Optional[str] = None,
        to_location: Optional[str] = None,
        driver_id: Optional[uuid.UUID] = None,
        id: Optional[uuid.UUID] = None,
    ):
        self.id = id
        self.name = name
        self.vehicle_number = vehicle_number
        self.starting_date = starting_date
        self.starting_time = starting_time
        self.available_seats = available_seats
        self.amount = amount
        self.from_location = from_location
        self.to_location = to_location
        self.driver_id = driver_id 