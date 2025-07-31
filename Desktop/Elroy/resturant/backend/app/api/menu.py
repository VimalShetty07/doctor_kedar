from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.restaurant import Restaurant
from app.models.menu_item import MenuItem
from app.schemas.restaurant import RestaurantResponse
from app.schemas.menu_item import MenuItemResponse

router = APIRouter(prefix="/menu", tags=["Menu"])


@router.get("/restaurant", response_model=RestaurantResponse)
def get_restaurant(db: Session = Depends(get_db)):
    """Get restaurant information"""
    restaurant = db.query(Restaurant).first()
    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found"
        )
    return restaurant


@router.get("/items", response_model=List[MenuItemResponse])
def get_menu_items(
    category: str = None,
    available_only: bool = True,
    db: Session = Depends(get_db)
):
    """Get all menu items with optional filtering"""
    query = db.query(MenuItem)
    
    if available_only:
        query = query.filter(MenuItem.is_available == True)
    
    if category:
        query = query.filter(MenuItem.category == category)
    
    items = query.all()
    return items


@router.get("/items/{item_id}", response_model=MenuItemResponse)
def get_menu_item(item_id: int, db: Session = Depends(get_db)):
    """Get a specific menu item"""
    item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu item not found"
        )
    return item


@router.get("/categories")
def get_categories(db: Session = Depends(get_db)):
    """Get all available categories"""
    categories = db.query(MenuItem.category).distinct().all()
    return [category[0] for category in categories if category[0]] 