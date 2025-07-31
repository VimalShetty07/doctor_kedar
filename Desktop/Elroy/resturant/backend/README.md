# Restaurant API Backend

FastAPI backend for the restaurant menu and ordering system with OTP authentication, cart management, and GST calculation.

## Features

- **OTP Authentication**: Phone-based login with JWT tokens
- **Restaurant Management**: Logo, banner, and restaurant information
- **Menu Management**: Food items with images, prices, and categories
- **Cart System**: Add, update, and remove items from cart
- **Order Processing**: Place orders with delivery address and special instructions
- **GST Calculation**: Automatic CGST and SGST calculation (18% total)
- **Bill Generation**: Detailed bills with tax breakdown
- **Local Development Ready**: Easy setup with environment variables

## Tech Stack

- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: Database ORM
- **PostgreSQL**: Primary database
- **Redis**: Caching and session management (optional)
- **Alembic**: Database migrations
- **JWT**: Token-based authentication

## Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL installed and running
- Redis (optional for local development)

### Local Development Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

5. **Set up PostgreSQL database:**
   ```bash
   # Create database
   createdb restaurant_db
   
   # Or using psql
   psql -U postgres
   CREATE DATABASE restaurant_db;
   \q
   ```

6. **Run the application:**
   ```bash
   # Option 1: Using the run script
   python run.py
   
   # Option 2: Using uvicorn directly
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

7. **Access the API:**
   - API: http://localhost:8000
   - Docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## Environment Variables

Create a `.env` file in the backend directory:

```env
# Database Configuration
DATABASE_URL=postgresql://postgres:password@localhost:5432/restaurant_db

# Security
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Redis Configuration (Optional for local development)
REDIS_URL=redis://localhost:6379

# Application Settings
DEBUG=True
ENVIRONMENT=development
CORS_ORIGINS=["http://localhost:3000"]

# GST Configuration
GST_PERCENTAGE=18.0
CGST_PERCENTAGE=9.0
SGST_PERCENTAGE=9.0
```

## Database Setup

### PostgreSQL Installation

**macOS (using Homebrew):**
```bash
brew install postgresql
brew services start postgresql
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

**Windows:**
Download and install from https://www.postgresql.org/download/windows/

### Create Database
```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE restaurant_db;

# Create user (optional)
CREATE USER restaurant_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE restaurant_db TO restaurant_user;

# Exit
\q
```

### Redis Setup (Optional)

**macOS:**
```bash
brew install redis
brew services start redis
```

**Ubuntu/Debian:**
```bash
sudo apt install redis-server
sudo systemctl start redis-server
```

**Windows:**
Download from https://redis.io/download

## API Documentation

### Authentication Endpoints

#### Register User
```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "name": "John Doe",
  "phone": "+919876543210"
}
```

#### Send OTP
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "phone": "+919876543210"
}
```

#### Verify OTP
```http
POST /api/v1/auth/verify-otp
Content-Type: application/json

{
  "phone": "+919876543210",
  "otp": "123456"
}
```

### Menu Endpoints

#### Get Restaurant Info
```http
GET /api/v1/menu/restaurant
```

#### Get Menu Items
```http
GET /api/v1/menu/items?category=main&available_only=true
```

#### Get Categories
```http
GET /api/v1/menu/categories
```

### Cart Endpoints

#### Get Cart
```http
GET /api/v1/cart/
Authorization: Bearer <token>
```

#### Add to Cart
```http
POST /api/v1/cart/add
Authorization: Bearer <token>
Content-Type: application/json

{
  "menu_item_id": 1,
  "quantity": 2
}
```

#### Update Cart Item
```http
PUT /api/v1/cart/update/1?quantity=3
Authorization: Bearer <token>
```

#### Remove from Cart
```http
DELETE /api/v1/cart/remove/1
Authorization: Bearer <token>
```

#### Clear Cart
```http
DELETE /api/v1/cart/clear
Authorization: Bearer <token>
```

### Order Endpoints

#### Place Order
```http
POST /api/v1/orders/place
Authorization: Bearer <token>
Content-Type: application/json

{
  "delivery_address": "123 Main St, City",
  "special_instructions": "Extra spicy please"
}
```

#### Get User Orders
```http
GET /api/v1/orders/
Authorization: Bearer <token>
```

#### Get Order Details
```http
GET /api/v1/orders/1
Authorization: Bearer <token>
```

#### Get Order Bill
```http
GET /api/v1/orders/1/bill
Authorization: Bearer <token>
```

## Database Models

### User
- `id`: Primary key
- `name`: User's full name
- `phone`: Phone number (unique)
- `otp`: Temporary OTP for verification
- `otp_expires_at`: OTP expiration time
- `is_verified`: Verification status
- `created_at`: Account creation time

### Restaurant
- `id`: Primary key
- `name`: Restaurant name
- `logo_url`: Restaurant logo URL
- `banner_url`: Restaurant banner URL
- `description`: Restaurant description
- `address`: Restaurant address
- `phone`: Contact phone
- `email`: Contact email

### MenuItem
- `id`: Primary key
- `name`: Item name
- `short_description`: Brief description
- `long_description`: Detailed description
- `price`: Item price
- `image_url`: Item image URL
- `is_available`: Availability status
- `category`: Item category
- `restaurant_id`: Foreign key to Restaurant

### Cart & CartItem
- `Cart`: User's shopping cart
- `CartItem`: Individual items in cart with quantities

### Order & OrderItem
- `Order`: Customer orders with GST calculation
- `OrderItem`: Individual items in order

## Database Migrations

### Initialize Alembic
```bash
alembic init alembic
```

### Create Migration
```bash
alembic revision --autogenerate -m "Add new table"
```

### Apply Migrations
```bash
alembic upgrade head
```

### Rollback Migration
```bash
alembic downgrade -1
```

## Development

### Code Formatting
```bash
# Format code
black .

# Sort imports
isort .

# Lint code
flake8 .

# Type checking
mypy .
```

### Testing
```bash
# Run tests
pytest

# Run with coverage
pytest --cov=app
```

### Database Operations
```bash
# Create tables (automatic on startup)
python -c "from app.database import create_tables; create_tables()"

# Reset database
python -c "from app.database import drop_tables; drop_tables()"
```

## API Response Examples

### Successful Login
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}
```

### Menu Items
```json
[
  {
    "id": 1,
    "name": "Butter Chicken",
    "short_description": "Creamy and rich Indian curry",
    "long_description": "Tender chicken cooked in a rich tomato and cream sauce...",
    "price": 350.0,
    "image_url": "https://example.com/butter-chicken.jpg",
    "is_available": true,
    "category": "Main Course",
    "restaurant_id": 1,
    "created_at": "2024-01-01T12:00:00Z"
  }
]
```

### Cart Response
```json
{
  "id": 1,
  "user_id": 1,
  "items": [
    {
      "id": 1,
      "menu_item_id": 1,
      "quantity": 2,
      "price_at_time": 350.0,
      "created_at": "2024-01-01T12:00:00Z",
      "menu_item": {
        "id": 1,
        "name": "Butter Chicken",
        "price": 350.0
      }
    }
  ],
  "total_items": 2,
  "subtotal": 700.0,
  "created_at": "2024-01-01T12:00:00Z"
}
```

### Order Response
```json
{
  "id": 1,
  "order_number": "ORD-ABC12345",
  "user_id": 1,
  "subtotal": 700.0,
  "cgst_amount": 63.0,
  "sgst_amount": 63.0,
  "gst_amount": 126.0,
  "total_amount": 826.0,
  "status": "pending",
  "delivery_address": "123 Main St, City",
  "special_instructions": "Extra spicy please",
  "items": [...],
  "created_at": "2024-01-01T12:00:00Z"
}
```

## Error Handling

The API returns standard HTTP status codes:

- `200`: Success
- `201`: Created
- `400`: Bad Request
- `401`: Unauthorized
- `404`: Not Found
- `422`: Validation Error
- `500`: Internal Server Error

Error responses include a `detail` field with the error message.

## Security Features

- JWT token authentication
- Password hashing with bcrypt
- CORS configuration
- Input validation with Pydantic
- SQL injection prevention with SQLAlchemy
- Environment variable protection

## Performance Optimizations

- Database connection pooling
- Efficient queries with SQLAlchemy
- Lazy loading of relationships
- Optimized for local development

## Monitoring and Logging

- Structured logging
- Health check endpoint
- Error tracking
- Performance metrics

## Troubleshooting

### Common Issues

1. **Database Connection Error:**
   - Ensure PostgreSQL is running
   - Check database credentials in `.env`
   - Verify database exists

2. **Import Errors:**
   - Activate virtual environment
   - Install dependencies: `pip install -r requirements.txt`

3. **Port Already in Use:**
   - Change port in `run.py` or use different port with uvicorn
   - Kill existing process: `lsof -ti:8000 | xargs kill -9`

4. **CORS Errors:**
   - Check CORS_ORIGINS in `.env`
   - Ensure frontend URL is included

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run linting and formatting
6. Submit a pull request

## License

This project is licensed under the MIT License. 