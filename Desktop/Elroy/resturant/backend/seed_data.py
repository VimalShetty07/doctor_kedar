#!/usr/bin/env python3
"""
Script to seed the database with dummy data
"""

import asyncio
from sqlalchemy.orm import Session
from app.database import SessionLocal, create_tables
from app.models import Restaurant, MenuItem, User, Table, TableStatus
from app.auth import generate_otp
from datetime import datetime, timedelta

def clear_all_data():
    """Clear all data in correct order"""
    db = SessionLocal()
    try:
        # Clear in reverse order of dependencies
        db.query(OrderItem).delete()
        db.query(Order).delete()
        db.query(CartItem).delete()
        db.query(Cart).delete()
        db.query(MenuItem).delete()
        db.query(Restaurant).delete()
        db.query(User).delete()
        db.query(Table).delete()
        db.commit()
        print("🗑️  Cleared all existing data")
    except Exception as e:
        print(f"❌ Error clearing data: {e}")
        db.rollback()
    finally:
        db.close()

def seed_restaurant():
    """Create a sample restaurant"""
    db = SessionLocal()
    try:
        restaurant = Restaurant(
            name="Spice Garden Restaurant",
            logo_url="https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=200&h=200&fit=crop",
            banner_url="https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=1200&h=400&fit=crop",
            description="Authentic Indian cuisine with a modern twist. We serve the finest dishes prepared with fresh ingredients and traditional recipes.",
            address="123 Main Street, Downtown, City - 123456",
            phone="+91-9876543210",
            email="info@spicegarden.com"
        )
        db.add(restaurant)
        db.commit()
        db.refresh(restaurant)
        print(f"✅ Created restaurant: {restaurant.name}")
        return restaurant
    except Exception as e:
        print(f"❌ Error creating restaurant: {e}")
        db.rollback()
        return None
    finally:
        db.close()

def seed_tables():
    """Create sample tables"""
    db = SessionLocal()
    try:
        tables = [
            {
                "table_number": "T1",
                "capacity": 4,
                "status": TableStatus.AVAILABLE,
                "qr_code_url": "https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=https://restaurant.com/table/T1"
            },
            {
                "table_number": "T2",
                "capacity": 6,
                "status": TableStatus.AVAILABLE,
                "qr_code_url": "https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=https://restaurant.com/table/T2"
            },
            {
                "table_number": "T3",
                "capacity": 4,
                "status": TableStatus.AVAILABLE,
                "qr_code_url": "https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=https://restaurant.com/table/T3"
            },
            {
                "table_number": "T4",
                "capacity": 8,
                "status": TableStatus.AVAILABLE,
                "qr_code_url": "https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=https://restaurant.com/table/T4"
            },
            {
                "table_number": "T5",
                "capacity": 2,
                "status": TableStatus.AVAILABLE,
                "qr_code_url": "https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=https://restaurant.com/table/T5"
            }
        ]
        
        for table_data in tables:
            table = Table(**table_data)
            db.add(table)
        
        db.commit()
        print(f"✅ Created {len(tables)} tables")
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        db.rollback()
    finally:
        db.close()

def seed_menu_items(restaurant_id: int):
    """Create sample menu items"""
    db = SessionLocal()
    try:
        menu_items = [
            {
                "name": "Butter Chicken",
                "short_description": "Creamy tomato-based curry with tender chicken",
                "long_description": "A classic Indian dish made with tender chicken pieces in a rich, creamy tomato-based curry sauce. Served with naan bread and rice.",
                "price": 350.00,
                "image_url": "https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=400&h=300&fit=crop",
                "is_available": True,
                "category": "Main Course"
            },
            {
                "name": "Paneer Tikka",
                "short_description": "Grilled cottage cheese with spices",
                "long_description": "Fresh cottage cheese marinated in yogurt and spices, grilled to perfection. Served with mint chutney and onion salad.",
                "price": 280.00,
                "image_url": "https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=400&h=300&fit=crop",
                "is_available": True,
                "category": "Appetizers"
            },
            {
                "name": "Biryani",
                "short_description": "Fragrant rice dish with aromatic spices",
                "long_description": "Aromatic basmati rice cooked with tender meat, fragrant spices, and herbs. Served with raita and papad.",
                "price": 450.00,
                "image_url": "https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=400&h=300&fit=crop",
                "is_available": True,
                "category": "Main Course"
            },
            {
                "name": "Dal Makhani",
                "short_description": "Creamy black lentils",
                "long_description": "Slow-cooked black lentils with cream and butter, seasoned with aromatic spices. A comfort food favorite.",
                "price": 180.00,
                "image_url": "https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=400&h=300&fit=crop",
                "is_available": True,
                "category": "Main Course"
            },
            {
                "name": "Naan Bread",
                "short_description": "Soft leavened flatbread",
                "long_description": "Soft and fluffy leavened flatbread, perfect for scooping up curries and gravies.",
                "price": 40.00,
                "image_url": "https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=400&h=300&fit=crop",
                "is_available": True,
                "category": "Breads"
            },
            {
                "name": "Gulab Jamun",
                "short_description": "Sweet milk solids in sugar syrup",
                "long_description": "Soft and spongy milk solids soaked in rose-flavored sugar syrup. A traditional Indian dessert.",
                "price": 120.00,
                "image_url": "https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=400&h=300&fit=crop",
                "is_available": True,
                "category": "Desserts"
            },
            {
                "name": "Masala Chai",
                "short_description": "Spiced Indian tea",
                "long_description": "Traditional Indian tea brewed with milk and aromatic spices like cardamom, ginger, and cinnamon.",
                "price": 60.00,
                "image_url": "https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=400&h=300&fit=crop",
                "is_available": True,
                "category": "Beverages"
            },
            {
                "name": "Raita",
                "short_description": "Cooling yogurt side dish",
                "long_description": "Fresh yogurt mixed with cucumber, mint, and spices. Perfect accompaniment to spicy dishes.",
                "price": 80.00,
                "image_url": "https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=400&h=300&fit=crop",
                "is_available": True,
                "category": "Sides"
            },
            {
                "name": "Chicken Curry",
                "short_description": "Spicy chicken in onion-tomato gravy",
                "long_description": "Tender chicken pieces cooked in a spicy onion-tomato gravy with aromatic spices. Served with rice or bread.",
                "price": 320.00,
                "image_url": "https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=400&h=300&fit=crop",
                "is_available": True,
                "category": "Main Course"
            },
            {
                "name": "Veg Thali",
                "short_description": "Complete vegetarian meal",
                "long_description": "A complete vegetarian meal with dal, vegetables, rice, bread, and accompaniments. Perfect for a wholesome lunch.",
                "price": 280.00,
                "image_url": "https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=400&h=300&fit=crop",
                "is_available": True,
                "category": "Thalis"
            }
        ]
        
        for item_data in menu_items:
            menu_item = MenuItem(
                restaurant_id=restaurant_id,
                **item_data
            )
            db.add(menu_item)
        
        db.commit()
        print(f"✅ Created {len(menu_items)} menu items")
        
    except Exception as e:
        print(f"❌ Error creating menu items: {e}")
        db.rollback()
    finally:
        db.close()

def seed_users():
    """Create sample users"""
    db = SessionLocal()
    try:
        users = [
            {
                "name": "John Doe",
                "phone": "+91-9876543210",
                "is_verified": True
            },
            {
                "name": "Jane Smith",
                "phone": "+91-9876543211",
                "is_verified": True
            },
            {
                "name": "Mike Johnson",
                "phone": "+91-9876543212",
                "is_verified": True
            }
        ]
        
        for user_data in users:
            user = User(
                **user_data,
                otp=generate_otp(),
                otp_expires_at=datetime.utcnow() + timedelta(minutes=10)
            )
            db.add(user)
        
        db.commit()
        print(f"✅ Created {len(users)} users")
        
    except Exception as e:
        print(f"❌ Error creating users: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    """Main function to seed all data"""
    print("🌱 Starting database seeding...")
    
    # Create tables if they don't exist
    create_tables()
    
    # Clear all existing data
    clear_all_data()
    
    # Seed restaurant
    restaurant = seed_restaurant()
    if restaurant:
        # Seed menu items
        seed_menu_items(restaurant.id)
    
    # Seed tables
    seed_tables()
    
    # Seed users
    seed_users()
    
    print("✅ Database seeding completed!")

if __name__ == "__main__":
    main() 