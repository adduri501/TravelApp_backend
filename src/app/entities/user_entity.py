from app.entities.mixin import CommonMixin
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, List, Optional, Type, TypeVar
from uuid import UUID
from dataclasses import asdict, dataclass, fields
import uuid

# @dataclass
# class UserEntity(CommonMixin):
#     id: uuid.UUID = field(default_factory=uuid.uuid4)

#     def __post_init__(self):
#         """Post initialization to set default role for users"""
#         if not self.role:
#             self.role = "passenger"  # Default role for travel app

#     @property
#     def is_driver(self) -> bool:
#         """Check if user is a driver"""
#         return self.role == "driver"

#     @property
#     def is_passenger(self) -> bool:
#         """Check if user is a passenger"""
#         return self.role == "passenger"

#     @property
#     def has_location(self) -> bool:
#         """Check if user has location data"""
#         return self.latitude is not None and self.longitude is not None

#     def set_location(self, latitude: float, longitude: float) -> None:
#         """Set user location"""
#         self.latitude = latitude
#         self.longitude = longitude
#         self.update_timestamp()

from datetime import datetime
import uuid


from dataclasses import dataclass
from datetime import datetime
import uuid


@dataclass
class UserEntity:
    mobile_number: str | None = None
    role: str | None = "passenger"
    name: str | None = None
    email: str | None = None
    alternative_mobile_number: str | None = None
    profile_pic: str | None = None
    gender: str | None = None
    id: uuid.UUID | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    username: str | None = None
    password_hash: str | None = None

    # Serialization Methods
    def to_dict(self, exclude: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Convert entity to dictionary with proper type handling.
        """
        exclude = set(exclude or [])
        result: Dict[str, Any] = {}

        for key, value in asdict(self).items():
            if key in exclude:
                continue
            if value is None:
                result[key] = None
            elif isinstance(value, UUID):
                result[key] = str(value)
            elif isinstance(value, datetime):
                result[key] = value.isoformat()
            else:
                result[key] = value
        return result
