from pydantic import BaseModel, EmailStr, Field, ConfigDict
from enum import Enum
import uuid
from uuid import UUID
from typing import Optional, Any
from datetime import datetime


class UserTypeEnum(str, Enum):
    passenger = "passenger"
    driver = "driver"
    admin = "admin"
    super_admin = "super_admin"


class SendOtpRequest(BaseModel):
    mobile_number: str = Field(..., min_length=10, max_length=15)
    user_type: str = Field(..., description="passenger/driver/admin/super_admin")
    device: str
    device_token: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    model_config = ConfigDict(extra="allow")


class SendOtpResponse(BaseModel):
    message: str
    success: bool
    expires_in: int  # seconds


class Gender(str, Enum):
    male = "male"
    female = "female"
    other = "other"
    not_given = "not_given"


class UserInputSchema(BaseModel):
    name: str
    email: EmailStr
    mobile_number: str
    alternative_mobile_number: str
    # profile_pic:str
    gender: Gender = Gender.not_given


class UserResponse(BaseModel):
    id: uuid.UUID
    name: str
    mobile_number: str
    email: EmailStr
    alternative_mobile_number: Optional[str] = None
    profile_pic: Optional[str] = None
    gender: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class VerifyOtpRequest(BaseModel):
    mobile_number: str
    otp_code: str
    device: str
    device_token: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    model_config = ConfigDict(extra="allow")


# class FileTranscriptionInputSchema(UserDetails):
#     file_data: UploadFile = File(
#         description="upload file for generating transcript", examples=["superior.mp4"]
#     )


class UserUpdateSchema(BaseModel):
    mobile_number: Optional[str] = None
    role: Optional[str] = None
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    alternative_mobile_number: Optional[str] = None
    profile_pic: Optional[str] = None
    gender: Optional[str] = None
    id: Optional[UUID] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
