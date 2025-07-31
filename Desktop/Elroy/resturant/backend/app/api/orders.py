from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.user import User
from app.models.order import Order, OrderItem, OrderStatus, OrderItemStatus
from app.models.menu_item import MenuItem
from app.models.cart import Cart, CartItem
from app.models.table_session import TableSession
from app.schemas.order import OrderCreate, OrderResponse, OrderItemResponse, Bill
from app.auth import get_current_user
from app.auth import generate_order_number, calculate_gst
from datetime import datetime
from app.models.restaurant import Restaurant
from app.models.table import Table

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/place", response_model=OrderResponse)
def place_order(
    order_data: OrderCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Place an order from cart"""
    # Check if user has an active table session
    session = db.query(TableSession).filter(
        TableSession.user_id == current_user.id,
        TableSession.is_active == True
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No active table session found. Please start a session first."
        )
    
    # Verify the session matches the order
    if session.id != order_data.table_session_id or session.table_id != order_data.table_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid table session for this order"
        )
    
    # Get user's cart
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart or not cart.items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cart is empty"
        )
    
    # Calculate totals
    subtotal = sum(item.quantity * item.price_at_time for item in cart.items)
    cgst_amount, sgst_amount, gst_amount = calculate_gst(subtotal)
    total_amount = subtotal + gst_amount
    
    # Create order with PENDING status
    order = Order(
        order_number=generate_order_number(),
        user_id=current_user.id,
        table_id=order_data.table_id,
        table_session_id=order_data.table_session_id,
        subtotal=subtotal,
        cgst_amount=cgst_amount,
        sgst_amount=sgst_amount,
        gst_amount=gst_amount,
        total_amount=total_amount,
        status=OrderStatus.PENDING,  # Order starts as pending
        delivery_address=order_data.delivery_address,
        special_instructions=order_data.special_instructions
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    
    # Create order items with PENDING status
    for cart_item in cart.items:
        order_item = OrderItem(
            order_id=order.id,
            menu_item_id=cart_item.menu_item_id,
            quantity=cart_item.quantity,
            price_at_time=cart_item.price_at_time,
            total_price=cart_item.quantity * cart_item.price_at_time,
            status=OrderItemStatus.PENDING  # Each item starts as pending
        )
        db.add(order_item)
    
    # Clear cart
    for item in cart.items:
        db.delete(item)
    
    db.commit()
    db.refresh(order)
    
    return order


@router.get("/", response_model=List[OrderResponse])
def get_user_orders(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get all orders for the current user"""
    orders = db.query(Order).filter(Order.user_id == current_user.id).all()
    return orders


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific order details"""
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id
    ).first()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    return order


@router.get("/{order_id}/bill", response_model=Bill)
def get_order_bill(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get bill for a specific order"""
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id
    ).first()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    # Get restaurant info
    restaurant = db.query(Restaurant).first()
    
    # Get order items with menu item details
    items = []
    for item in order.items:
        menu_item = db.query(MenuItem).filter(MenuItem.id == item.menu_item_id).first()
        items.append({
            "name": menu_item.name if menu_item else "Unknown Item",
            "quantity": item.quantity,
            "price": item.price_at_time,
            "total": item.total_price,
            "status": item.status.value
        })
    
    # Get table info
    table = db.query(Table).filter(Table.id == order.table_id).first()
    
    return Bill(
        order_number=order.order_number,
        order_date=order.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        restaurant_name=restaurant.name if restaurant else "Restaurant",
        restaurant_address=restaurant.address if restaurant else "",
        customer_name=current_user.name or "Guest",
        customer_phone=current_user.phone,
        table_number=table.table_number if table else "",
        delivery_address=order.delivery_address,
        items=items,
        subtotal=order.subtotal,
        cgst_amount=order.cgst_amount,
        sgst_amount=order.sgst_amount,
        gst_amount=order.gst_amount,
        total_amount=order.total_amount,
        status=order.status.value,
        special_instructions=order.special_instructions
    ) 