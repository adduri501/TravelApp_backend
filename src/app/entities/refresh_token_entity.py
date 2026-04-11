from dataclasses import dataclass
from datetime import datetime
import uuid
from typing import Optional


@dataclass
class RefreshTokenEntity:
    user_id: uuid.UUID
    token_jti: str
    device_id: uuid.UUID 
    expires_at: datetime
    is_revoked: bool = False
    # device_id: uuid.UUID | None = None
    created_at: Optional[datetime] = None
    id: Optional[uuid.UUID] | None = None
