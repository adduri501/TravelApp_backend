

from dataclasses import dataclass,field,asdict,fields

from uuid import UUID,uuid4
from typing import Any, ClassVar, Dict, List, Optional, Type, TypeVar
from datetime import datetime


@dataclass
class CommonMixin:
    name: Optional[str] = field(default=None)
    mobile_number: str = field(default="")
    email: Optional[str] = field(default=None)
    alternative_mobile_number: Optional[str] = field(default=None)
    profile_pic: Optional[str] = field(default=None)
    gender: Optional[str] = field(default=None)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    device_token: Optional[str] = field(default=None)
    latitude: Optional[float] = field(default=None)
    longitude: Optional[float] = field(default=None)
    role: str = field(default="user")

    def to_dict(self) -> Dict[str, Any]:
        """Convert entity to dictionary"""
        return {
            field.name: getattr(self, field.name) 
            for field in fields(self)
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CommonMixin':
        """Create entity from dictionary"""
        field_names = {f.name for f in fields(cls)}
        filtered_data = {k: v for k, v in data.items() if k in field_names}
        return cls(**filtered_data)

    def update_timestamp(self) -> None:
        """Update the updated_at timestamp"""
        self.updated_at = datetime.utcnow()
    

    




    
