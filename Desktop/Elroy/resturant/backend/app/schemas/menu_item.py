from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class MenuItemCreate(BaseModel):
    name: str
    short_description: Optional[str] = None
    long_description: Optional[str] = None
    price: float
    image_url: Optional[str] = None
    is_available: bool = True
    category: Optional[str] = None
    restaurant_id: int


class MenuItemResponse(BaseModel):
    id: int
    name: str
    short_description: Optional[str] = None
    long_description: Optional[str] = None
    price: float
    image_url: Optional[str] = None
    is_available: bool
    category: Optional[str] = None
    restaurant_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True 