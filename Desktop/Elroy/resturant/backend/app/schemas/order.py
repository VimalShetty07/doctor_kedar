from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum


class OrderStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    PREPARING = "preparing"
    READY = "ready"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class OrderItemStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    PREPARING = "preparing"
    READY = "ready"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class OrderItemResponse(BaseModel):
    id: int
    menu_item_id: int
    quantity: int
    price_at_time: float
    total_price: float
    status: OrderItemStatus
    admin_notes: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    menu_item: Optional[dict] = None
    
    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    table_id: int
    table_session_id: int
    delivery_address: Optional[str] = None
    special_instructions: Optional[str] = None


class OrderResponse(BaseModel):
    id: int
    order_number: str
    user_id: int
    table_id: int
    table_session_id: int
    subtotal: float
    cgst_amount: float
    sgst_amount: float
    gst_amount: float
    total_amount: float
    status: OrderStatus
    delivery_address: Optional[str] = None
    special_instructions: Optional[str] = None
    admin_notes: Optional[str] = None
    items: List[OrderItemResponse]
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class OrderStatusUpdate(BaseModel):
    status: OrderStatus
    admin_notes: Optional[str] = None


class OrderItemStatusUpdate(BaseModel):
    status: OrderItemStatus
    admin_notes: Optional[str] = None


class Bill(BaseModel):
    order_number: str
    order_date: str
    restaurant_name: str
    restaurant_address: str
    customer_name: str
    customer_phone: str
    table_number: str
    delivery_address: Optional[str] = None
    items: List[dict]
    subtotal: float
    cgst_amount: float
    sgst_amount: float
    gst_amount: float
    total_amount: float
    status: str
    special_instructions: Optional[str] = None 