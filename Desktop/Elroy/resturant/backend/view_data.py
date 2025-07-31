#!/usr/bin/env python3
"""
Script to view the seeded data in the database
"""

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Restaurant, MenuItem, User

def view_restaurant():
    """View restaurant data"""
    db = SessionLocal()
    try:
        restaurant = db.query(Restaurant).first()
        if restaurant:
            print("🏪 RESTAURANT:")
            print(f"   Name: {restaurant.name}")
            print(f"   Address: {restaurant.address}")
            print(f"   Phone: {restaurant.phone}")
            print(f"   Email: {restaurant.email}")
            print(f"   Description: {restaurant.description}")
            print()
        else:
            print("❌ No restaurant found")
    except Exception as e:
        print(f"❌ Error viewing restaurant: {e}")
    finally:
        db.close()

def view_menu_items():
    """View menu items"""
    db = SessionLocal()
    try:
        menu_items = db.query(MenuItem).all()
        if menu_items:
            print("🍽️  MENU ITEMS:")
            for item in menu_items:
                print(f"   • {item.name} - ₹{item.price}")
                print(f"     Category: {item.category}")
                print(f"     Available: {'Yes' if item.is_available else 'No'}")
                print()
        else:
            print("❌ No menu items found")
    except Exception as e:
        print(f"❌ Error viewing menu items: {e}")
    finally:
        db.close()

def view_users():
    """View users"""
    db = SessionLocal()
    try:
        users = db.query(User).all()
        if users:
            print("👥 USERS:")
            for user in users:
                print(f"   • {user.name} - {user.phone}")
                print(f"     Verified: {'Yes' if user.is_verified else 'No'}")
                print()
        else:
            print("❌ No users found")
    except Exception as e:
        print(f"❌ Error viewing users: {e}")
    finally:
        db.close()

def main():
    """Main function to view all data"""
    print("📊 DATABASE CONTENTS:")
    print("=" * 50)
    
    view_restaurant()
    view_menu_items()
    view_users()

if __name__ == "__main__":
    main() 