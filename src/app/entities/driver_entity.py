from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import uuid


@dataclass
class DriverEntity:
    user_id: uuid.UUID
    vehicle_number: Optional[str] = None
    license_number: Optional[str] = None
    name: Optional[str] = None
    address: Optional[str] = None
    aadhaar_number: Optional[str] = None
    is_verified: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    id: Optional[uuid.UUID] = None