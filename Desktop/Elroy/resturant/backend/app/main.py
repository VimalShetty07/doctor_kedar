from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import create_tables
from app.api import auth, menu, cart, orders, tables, admin
from app.config import settings

# Create tables
create_tables()

# Create FastAPI app
app = FastAPI(
    title="Restaurant Table Booking API",
    description="API for restaurant table booking and ordering system",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(menu.router, prefix="/api/v1")
app.include_router(cart.router, prefix="/api/v1")
app.include_router(orders.router, prefix="/api/v1")
app.include_router(tables.router, prefix="/api/v1")
app.include_router(admin.router, prefix="/api/v1")


@app.get("/")
def read_root():
    return {
        "message": "Restaurant Table Booking API",
        "version": "1.0.0",
        "environment": settings.environment
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "environment": settings.environment
    } 