from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.order import Order, OrderItem, OrderStatus, OrderItemStatus
from app.models.user import User
from app.schemas.order import OrderResponse, OrderStatusUpdate, OrderItemStatusUpdate, OrderItemResponse
from app.auth import get_current_user
from datetime import datetime

router = APIRouter(prefix="/admin", tags=["Admin"])


def get_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """Verify user is admin (you can add admin role logic here)"""
    # For now, we'll allow any authenticated user to be admin
    # In production, you should check for admin role
    return current_user


@router.get("/orders", response_model=List[OrderResponse])
def get_all_orders(
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Get all orders for admin"""
    orders = db.query(Order).order_by(Order.created_at.desc()).all()
    return orders


@router.get("/orders/pending", response_model=List[OrderResponse])
def get_pending_orders(
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Get all pending orders"""
    orders = db.query(Order).filter(
        Order.status == OrderStatus.PENDING
    ).order_by(Order.created_at.asc()).all()
    return orders


@router.get("/orders/{order_id}", response_model=OrderResponse)
def get_order_details(
    order_id: int,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Get specific order details for admin"""
    order = db.query(Order).filter(Order.id == order_id).first()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    return order


@router.patch("/orders/{order_id}/status", response_model=OrderResponse)
def update_order_status(
    order_id: int,
    status_update: OrderStatusUpdate,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Update order status"""
    order = db.query(Order).filter(Order.id == order_id).first()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    order.status = status_update.status
    order.admin_notes = status_update.admin_notes
    order.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(order)
    
    return order


@router.patch("/orders/{order_id}/items/{item_id}/status", response_model=OrderItemResponse)
def update_order_item_status(
    order_id: int,
    item_id: int,
    status_update: OrderItemStatusUpdate,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Update specific order item status"""
    order_item = db.query(OrderItem).filter(
        OrderItem.id == item_id,
        OrderItem.order_id == order_id
    ).first()
    
    if not order_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order item not found"
        )
    
    order_item.status = status_update.status
    order_item.admin_notes = status_update.admin_notes
    order_item.updated_at = datetime.utcnow()
    
    # Update order status based on item statuses
    order = db.query(Order).filter(Order.id == order_id).first()
    if order:
        all_items = db.query(OrderItem).filter(OrderItem.order_id == order_id).all()
        
        # Check if all items are ready
        if all(item.status == OrderItemStatus.READY for item in all_items):
            order.status = OrderStatus.READY
        # Check if any item is being prepared
        elif any(item.status == OrderItemStatus.PREPARING for item in all_items):
            order.status = OrderStatus.PREPARING
        # Check if all items are accepted
        elif all(item.status in [OrderItemStatus.ACCEPTED, OrderItemStatus.PREPARING, OrderItemStatus.READY] for item in all_items):
            order.status = OrderStatus.ACCEPTED
        
        order.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(order_item)
    
    return order_item


@router.get("/orders/{order_id}/items", response_model=List[OrderItemResponse])
def get_order_items(
    order_id: int,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Get all items for a specific order"""
    order_items = db.query(OrderItem).filter(
        OrderItem.order_id == order_id
    ).all()
    
    if not order_items:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found or has no items"
        )
    
    return order_items


@router.post("/orders/{order_id}/accept")
def accept_order(
    order_id: int,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Accept an order and all its items"""
    order = db.query(Order).filter(Order.id == order_id).first()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    if order.status != OrderStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order is not in pending status"
        )
    
    # Update order status
    order.status = OrderStatus.ACCEPTED
    order.updated_at = datetime.utcnow()
    
    # Update all items to accepted
    order_items = db.query(OrderItem).filter(OrderItem.order_id == order_id).all()
    for item in order_items:
        item.status = OrderItemStatus.ACCEPTED
        item.updated_at = datetime.utcnow()
    
    db.commit()
    
    return {"message": "Order accepted successfully"}


@router.post("/orders/{order_id}/ready")
def mark_order_ready(
    order_id: int,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Mark order as ready for delivery"""
    order = db.query(Order).filter(Order.id == order_id).first()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    if order.status not in [OrderStatus.ACCEPTED, OrderStatus.PREPARING]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order is not in accepted or preparing status"
        )
    
    # Update order status
    order.status = OrderStatus.READY
    order.updated_at = datetime.utcnow()
    
    # Update all items to ready
    order_items = db.query(OrderItem).filter(OrderItem.order_id == order_id).all()
    for item in order_items:
        if item.status != OrderItemStatus.CANCELLED:
            item.status = OrderItemStatus.READY
            item.updated_at = datetime.utcnow()
    
    db.commit()
    
    return {"message": "Order marked as ready"}


@router.post("/orders/{order_id}/deliver")
def deliver_order(
    order_id: int,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Mark order as delivered"""
    order = db.query(Order).filter(Order.id == order_id).first()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    if order.status != OrderStatus.READY:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order is not ready for delivery"
        )
    
    # Update order status
    order.status = OrderStatus.DELIVERED
    order.updated_at = datetime.utcnow()
    
    # Update all items to delivered
    order_items = db.query(OrderItem).filter(OrderItem.order_id == order_id).all()
    for item in order_items:
        if item.status != OrderItemStatus.CANCELLED:
            item.status = OrderItemStatus.DELIVERED
            item.updated_at = datetime.utcnow()
    
    db.commit()
    
    return {"message": "Order delivered successfully"} 