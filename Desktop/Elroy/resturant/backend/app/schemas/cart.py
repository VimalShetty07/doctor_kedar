from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class CartItemCreate(BaseModel):
    menu_item_id: int
    quantity: int = 1


class CartItemResponse(BaseModel):
    id: int
    menu_item_id: int
    quantity: int
    price_at_time: float
    created_at: datetime
    menu_item: Optional[dict] = None
    
    class Config:
        from_attributes = True


class CartResponse(BaseModel):
    id: int
    user_id: int
    items: List[CartItemResponse]
    total_items: int
    subtotal: float
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True 