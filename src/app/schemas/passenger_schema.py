from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID


class PassengerInputSchema(BaseModel):
    user_id: UUID
    name: Optional[str] = None
    email: Optional[EmailStr] = None



class PassengerUpdateSchema(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None