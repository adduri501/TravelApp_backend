from dataclasses import dataclass
from datetime import datetime
import uuid


@dataclass
class UserDeviceEntity:
    user_id: uuid.UUID
    device: str | None = None
    device_token: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    last_login: datetime | None = None
    created_at: datetime | None = None
    id: uuid.UUID | None = None
