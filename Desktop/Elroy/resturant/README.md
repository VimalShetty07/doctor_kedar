# Restaurant Menu & Ordering System

A full-stack restaurant menu and ordering application with OTP authentication, cart management, and GST calculation.

## Features

### Backend (FastAPI)
- **OTP Authentication**: Phone-based login with OTP verification
- **Restaurant Management**: Logo, banner, and restaurant information
- **Menu Management**: Food items with images, prices, descriptions, and categories
- **Cart System**: Add, update, and remove items from cart
- **Order Processing**: Place orders with delivery address and special instructions
- **GST Calculation**: Automatic CGST and SGST calculation (18% total)
- **Bill Generation**: Detailed bills with tax breakdown
- **Local Development Ready**: Easy setup with environment variables

### Frontend (Next.js)
- **Modern UI**: Responsive design with Tailwind CSS
- **Authentication**: OTP-based login flow
- **Menu Browsing**: Category filtering and item details
- **Shopping Cart**: Quantity management and cart operations
- **Order Management**: Order history and detailed views
- **Bill Display**: Printable bills with GST breakdown
- **Production Optimized**: TypeScript, ESLint, optimized builds

## Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: Database ORM
- **PostgreSQL**: Primary database
- **Redis**: Caching and session management (optional)
- **Alembic**: Database migrations
- **JWT**: Token-based authentication

### Frontend
- **Next.js 14**: React framework with App Router
- **TypeScript**: Type safety
- **Tailwind CSS**: Utility-first CSS framework
- **Axios**: HTTP client
- **React Hot Toast**: Notifications
- **Lucide React**: Icons

## Project Structure

```
restaurant/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── models/         # Database models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── config.py       # Configuration
│   │   ├── database.py     # Database setup
│   │   └── auth.py         # Authentication
│   ├── requirements.txt    # Python dependencies
│   ├── run.py             # Local development runner
│   └── README.md          # Backend documentation
├── frontend/               # Next.js frontend
│   ├── src/
│   │   ├── app/           # App Router pages
│   │   ├── components/    # React components
│   │   ├── hooks/         # Custom hooks
│   │   ├── lib/           # Utilities
│   │   └── types/         # TypeScript types
│   ├── package.json       # Node dependencies
│   └── README.md          # Frontend documentation
├── setup.sh               # Quick setup script
└── README.md              # This file
```

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+ and npm
- PostgreSQL installed and running

### Backend Setup

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
   # Edit .env with your database configuration
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
   python run.py
   ```

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Run development server:**
   ```bash
   npm run dev
   ```

4. **Build for production:**
   ```bash
   npm run build
   npm start
   ```

## Environment Variables

### Backend (.env)
```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/restaurant_db
SECRET_KEY=your-secret-key
DEBUG=True
ENVIRONMENT=development
CORS_ORIGINS=["http://localhost:3000"]
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
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

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Send OTP
- `POST /api/v1/auth/verify-otp` - Verify OTP and get token

### Menu
- `GET /api/v1/menu/restaurant` - Get restaurant info
- `GET /api/v1/menu/items` - Get menu items
- `GET /api/v1/menu/categories` - Get categories

### Cart
- `GET /api/v1/cart/` - Get user's cart
- `POST /api/v1/cart/add` - Add item to cart
- `PUT /api/v1/cart/update/{item_id}` - Update item quantity
- `DELETE /api/v1/cart/remove/{item_id}` - Remove item
- `DELETE /api/v1/cart/clear` - Clear cart

### Orders
- `POST /api/v1/orders/place` - Place new order
- `GET /api/v1/orders/` - Get user's orders
- `GET /api/v1/orders/{order_id}` - Get order details
- `GET /api/v1/orders/{order_id}/bill` - Get order bill

## Features in Detail

### OTP Authentication
- Phone number registration
- 6-digit OTP generation
- JWT token-based sessions
- Secure token storage

### Menu System
- Restaurant branding (logo, banner)
- Food categories
- Item images and descriptions
- Price management
- Availability status

### Cart Management
- Add/remove items
- Quantity updates
- Price calculations
- Persistent cart state

### Order Processing
- Delivery address collection
- Special instructions
- GST calculation (CGST 9% + SGST 9%)
- Order status tracking
- Bill generation

### Bill Features
- Detailed item breakdown
- Tax calculations
- Printable format
- Order tracking
- Customer information

## Development

### Database Migrations
```bash
# Create new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head
```

### Code Formatting
```bash
# Backend
black .
isort .

# Frontend
npm run lint
npm run format
```

### Running the Application

**Backend:**
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python run.py
```

**Frontend:**
```bash
cd frontend
npm run dev
```

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
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License. 