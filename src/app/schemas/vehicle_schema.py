# app/schemas/vehicle_schema.py

from pydantic import BaseModel
from typing import Optional


class VehicleBase(BaseModel):
    vehicle_number: str
    vehicle_name: Optional[str] = None
    color: Optional[str] = None
    no_of_seats: Optional[int] = None

class CreateVehicleRequest(VehicleBase):
    pass


class UpdateVehicleRequest(BaseModel):
   vehicle_number: Optional[str] = None
   vehicle_name: Optional[str] = None
   color: Optional[str] = None
   no_of_seats: Optional[int] = None
   is_active: Optional[bool] = None