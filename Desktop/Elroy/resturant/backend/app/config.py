from pydantic_settings import BaseSettings
from typing import List, Optional
import os


class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://postgres:password@localhost:5432/restaurant_db"
    database_test_url: str = "postgresql://postgres:password@localhost:5432/restaurant_test_db"
    
    # Security
    secret_key: str = "your-secret-key-here-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Redis (Optional for local development)
    redis_url: Optional[str] = "redis://localhost:6379"
    
    # AWS S3 (Optional for local development)
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    aws_region: str = "us-east-1"
    aws_s3_bucket: str = "restaurant-images"
    
    # SMS (Optional for local development)
    twilio_account_sid: str = ""
    twilio_auth_token: str = ""
    twilio_phone_number: str = ""
    
    # Application
    debug: bool = True
    environment: str = "development"
    cors_origins: List[str] = ["http://localhost:3000"]
    
    # GST Configuration
    gst_percentage: float = 18.0
    cgst_percentage: float = 9.0
    sgst_percentage: float = 9.0
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings() 