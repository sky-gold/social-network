from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional
import uuid

class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr

class UserLogin(BaseModel):
    username: str
    password: str

class ProfileBase(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    phone_number: Optional[str] = None

class ProfileUpdate(ProfileBase):
    email: Optional[EmailStr] = None

class ProfileResponse(ProfileBase):
    username: str
    email: EmailStr
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)

class SessionResponse(BaseModel):
    session_id: uuid.UUID
    user_id: uuid.UUID
    expires_at: datetime
    ip_address: str
    created_at: datetime

    class Config:
        orm_mode = True
