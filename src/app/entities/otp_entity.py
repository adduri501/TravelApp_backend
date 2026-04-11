from datetime import datetime
import uuid
from dataclasses import dataclass
from datetime import datetime
import uuid


@dataclass
class OtpEntity:
    mobile_number: str
    otp: str
    expire_at: datetime
    is_used: bool = False
    attempted_count: int = 0
    id: uuid.UUID | None = None


