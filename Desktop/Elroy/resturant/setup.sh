#!/bin/bash

echo "🚀 Setting up Restaurant Menu & Ordering System"
echo "================================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11+ first."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ first."
    exit 1
fi

# Check if PostgreSQL is installed
if ! command -v psql &> /dev/null; then
    echo "⚠️  PostgreSQL is not installed. Please install PostgreSQL first."
    echo "   macOS: brew install postgresql"
    echo "   Ubuntu: sudo apt install postgresql postgresql-contrib"
    echo "   Windows: Download from https://www.postgresql.org/download/windows/"
fi

echo "✅ Prerequisites check passed"

# Backend setup
echo ""
echo "📦 Setting up Backend..."
cd backend

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv

# Activate virtual environment
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp env.example .env
    echo "⚠️  Please edit backend/.env with your database configuration"
fi

cd ..

# Frontend setup
echo ""
echo "📦 Setting up Frontend..."
cd frontend

# Install dependencies
echo "Installing Node.js dependencies..."
npm install

# Create .env.local file if it doesn't exist
if [ ! -f .env.local ]; then
    echo "Creating .env.local file..."
    echo "NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1" > .env.local
fi

cd ..

echo ""
echo "✅ Setup completed!"
echo ""
echo "🎯 Next steps:"
echo "1. Install and start PostgreSQL"
echo "2. Create database: createdb restaurant_db"
echo "3. Edit backend/.env with your database credentials"
echo "4. Start the backend: cd backend && python run.py"
echo "5. Start the frontend: cd frontend && npm run dev"
echo ""
echo "🌐 Access your application:"
echo "- Frontend: http://localhost:3000"
echo "- Backend API: http://localhost:8000"
echo "- API Docs: http://localhost:8000/docs"
echo ""
echo "📚 For more information, check the README files in backend/ and frontend/ directories." 