from pydantic import BaseModel, Field
from typing import Optional


class DriverBase(BaseModel):
    name: Optional[str] = Field(None, max_length=255)

    license_number: Optional[str] = Field(
        None, max_length=100, description="Driving license number"
    )

    vehicle_number: Optional[str] = Field(
        None, max_length=50, description="Vehicle registration number"
    )

    address: Optional[str] = Field(
        None, max_length=500
    )

    aadhaar_number: Optional[str] = Field(
        None, min_length=12, max_length=12,
        description="12-digit Aadhaar number"
    )

class CreateDriverRequest(DriverBase):
    pass


class UpdateDriverRequest(DriverBase):
    pass

class VerifyDriverRequest(BaseModel):
    user_id: str  # or UUID if you prefer
    #Used by admin

