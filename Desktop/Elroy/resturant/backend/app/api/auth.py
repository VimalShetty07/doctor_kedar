from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import PhoneLogin, OTPVerify, UserResponse, Token
from app.auth import create_access_token, generate_otp, is_otp_expired
from app.config import settings

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/phone-login")
def phone_login(phone_data: PhoneLogin, db: Session = Depends(get_db)):
    """Send OTP for login/registration - creates user if doesn't exist"""
    phone = phone_data.phone
    
    # Check if user exists
    user = db.query(User).filter(User.phone == phone).first()
    
    if not user:
        # Create new user if doesn't exist
        user = User(
            phone=phone,
            name=None,  # Will be set later if needed
            is_verified=False
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        print(f"🆕 Created new user with phone: {phone}")
    
    # Generate OTP
    otp = generate_otp()
    otp_expires_at = datetime.utcnow() + timedelta(minutes=5)
    
    # Update user with OTP
    user.otp = otp
    user.otp_expires_at = otp_expires_at
    db.commit()
    
    # Print OTP for development
    print(f"📱 OTP for {phone}: {otp}")
    
    # In production, send OTP via SMS
    # For development, we'll return the OTP in response
    return {
        "message": "OTP sent successfully",
        "phone": phone,
        "otp": otp,  # Remove this in production
        "is_new_user": user.name is None
    }


@router.post("/verify-otp", response_model=Token)
def verify_otp(otp_data: OTPVerify, db: Session = Depends(get_db)):
    """Verify OTP and return access token"""
    user = db.query(User).filter(User.phone == otp_data.phone).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if OTP matches and is not expired
    if user.otp != otp_data.otp:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid OTP"
        )
    
    if is_otp_expired(user.otp_expires_at):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="OTP has expired"
        )
    
    # Mark user as verified and clear OTP
    user.is_verified = True
    user.otp = None
    user.otp_expires_at = None
    db.commit()
    
    # Create access token
    access_token = create_access_token(data={"sub": user.phone})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    } 