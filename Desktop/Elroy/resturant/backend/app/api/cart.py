from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.cart import Cart, CartItem
from app.models.menu_item import MenuItem
from app.schemas.cart import CartItemCreate, CartResponse, CartItemResponse
from app.schemas.menu_item import MenuItemResponse
from app.auth import get_current_user

router = APIRouter(prefix="/cart", tags=["Cart"])


def get_or_create_cart(user: User, db: Session) -> Cart:
    """Get existing cart or create new one for user"""
    cart = db.query(Cart).filter(Cart.user_id == user.id).first()
    if not cart:
        cart = Cart(user_id=user.id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart


@router.get("/", response_model=CartResponse)
def get_cart(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get user's cart"""
    cart = get_or_create_cart(current_user, db)
    
    # Calculate totals
    total_items = sum(item.quantity for item in cart.items)
    subtotal = sum(item.quantity * item.price_at_time for item in cart.items)
    
    # Convert to response model
    cart_items = []
    for item in cart.items:
        # Get menu item details
        menu_item = db.query(MenuItem).filter(MenuItem.id == item.menu_item_id).first()
        menu_item_response = MenuItemResponse.from_orm(menu_item) if menu_item else None
        
        cart_item_response = CartItemResponse(
            id=item.id,
            menu_item_id=item.menu_item_id,
            quantity=item.quantity,
            price_at_time=item.price_at_time,
            created_at=item.created_at,
            menu_item=menu_item_response.dict() if menu_item_response else None
        )
        cart_items.append(cart_item_response)
    
    return CartResponse(
        id=cart.id,
        user_id=cart.user_id,
        items=cart_items,
        total_items=total_items,
        subtotal=subtotal,
        created_at=cart.created_at,
        updated_at=cart.updated_at
    )


@router.post("/add", response_model=CartResponse)
def add_to_cart(
    item_data: CartItemCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add item to cart"""
    # Check if menu item exists and is available
    menu_item = db.query(MenuItem).filter(
        MenuItem.id == item_data.menu_item_id,
        MenuItem.is_available == True
    ).first()
    
    if not menu_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu item not found or not available"
        )
    
    cart = get_or_create_cart(current_user, db)
    
    # Check if item already exists in cart
    existing_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.menu_item_id == item_data.menu_item_id
    ).first()
    
    if existing_item:
        # Update quantity
        existing_item.quantity += item_data.quantity
        existing_item.price_at_time = menu_item.price
    else:
        # Add new item
        cart_item = CartItem(
            cart_id=cart.id,
            menu_item_id=item_data.menu_item_id,
            quantity=item_data.quantity,
            price_at_time=menu_item.price
        )
        db.add(cart_item)
    
    db.commit()
    db.refresh(cart)
    
    # Return updated cart using the same logic as get_cart
    return get_cart(current_user, db)


@router.put("/update/{item_id}")
def update_cart_item(
    item_id: int,
    quantity: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update cart item quantity"""
    cart = get_or_create_cart(current_user, db)
    
    cart_item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.cart_id == cart.id
    ).first()
    
    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found"
        )
    
    if quantity <= 0:
        db.delete(cart_item)
    else:
        cart_item.quantity = quantity
    
    db.commit()
    
    return {"message": "Cart updated successfully"}


@router.delete("/remove/{item_id}")
def remove_from_cart(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Remove item from cart"""
    cart = get_or_create_cart(current_user, db)
    
    cart_item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.cart_id == cart.id
    ).first()
    
    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found"
        )
    
    db.delete(cart_item)
    db.commit()
    
    return {"message": "Item removed from cart"}


@router.delete("/clear")
def clear_cart(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Clear all items from cart"""
    cart = get_or_create_cart(current_user, db)
    
    for item in cart.items:
        db.delete(item)
    
    db.commit()
    
    return {"message": "Cart cleared successfully"} 