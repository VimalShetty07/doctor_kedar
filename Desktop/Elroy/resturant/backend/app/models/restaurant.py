from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class Restaurant(Base):
    __tablename__ = "restaurants"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    logo_url = Column(String(500), nullable=True)
    banner_url = Column(String(500), nullable=True)
    description = Column(Text, nullable=True)
    address = Column(Text, nullable=True)
    phone = Column(String(15), nullable=True)
    email = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    menu_items = relationship("MenuItem", back_populates="restaurant") 