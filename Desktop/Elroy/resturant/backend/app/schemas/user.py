from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class PhoneLogin(BaseModel):
    phone: str


class OTPVerify(BaseModel):
    phone: str
    otp: str


class UserResponse(BaseModel):
    id: int
    name: Optional[str] = None
    phone: str
    is_verified: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse


class TokenData(BaseModel):
    phone: Optional[str] = None 