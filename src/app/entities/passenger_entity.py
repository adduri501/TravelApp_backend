from dataclasses import dataclass
from datetime import datetime
import uuid
from typing import Optional


@dataclass
class PassengerEntity:
    user_id: uuid.UUID
    name: Optional[str] = None
    email: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    id: Optional[uuid.UUID] = None
