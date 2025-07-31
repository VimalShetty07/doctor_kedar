from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class RestaurantCreate(BaseModel):
    name: str
    logo_url: Optional[str] = None
    banner_url: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None


class RestaurantResponse(BaseModel):
    id: int
    name: str
    logo_url: Optional[str] = None
    banner_url: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True 