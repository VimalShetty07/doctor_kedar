from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum


class TableStatus(str, Enum):
    AVAILABLE = "available"
    OCCUPIED = "occupied"
    RESERVED = "reserved"
    CLEANING = "cleaning"


class TableBase(BaseModel):
    table_number: str
    capacity: int = 4
    status: TableStatus = TableStatus.AVAILABLE
    qr_code_url: Optional[str] = None


class TableCreate(TableBase):
    pass


class TableResponse(TableBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class TableSessionBase(BaseModel):
    table_id: int
    user_id: int


class TableSessionCreate(TableSessionBase):
    pass


class TableSessionResponse(TableSessionBase):
    id: int
    session_start: datetime
    session_end: Optional[datetime] = None
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class TableWithSession(BaseModel):
    table: TableResponse
    current_session: Optional[TableSessionResponse] = None
    
    class Config:
        from_attributes = True 