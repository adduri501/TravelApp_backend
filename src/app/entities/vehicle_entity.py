from typing import Optional
import uuid
from datetime import datetime


class VehicleEntity:
    def __init__(
        self,
        vehicle_number: str,
        vehicle_name: Optional[str] = None,
        color: Optional[str] = None,
        no_of_seats: Optional[int] = None,
        is_active: bool = True,
        id: Optional[uuid.UUID] = None,
        created_at: Optional[datetime] = None,   
        updated_at: Optional[datetime] = None,  
    ):
        self.id = id
        self.vehicle_number = vehicle_number
        self.vehicle_name = vehicle_name
        self.color = color
        self.no_of_seats = no_of_seats
        self.is_active = is_active
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self):
        return {
            "id": str(self.id) if self.id else None,
            "vehicle_number": self.vehicle_number,
            "vehicle_name": self.vehicle_name,
            "color": self.color,
            "no_of_seats": self.no_of_seats,
            "is_active": self.is_active,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }