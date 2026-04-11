from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CreateAdminRequest(BaseModel):
    username: str
    password: str
    name: Optional[str] = None



class CreateDriverRequest(BaseModel):
    mobile_number: str
    license_number: str
    aadhaar_number: str

    name: Optional[str] = None
    profile_pic: Optional[str] = None
    gender: Optional[str] = None
    dob: Optional[datetime] = None