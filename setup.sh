#!/bin/bash

# Resume Parser Setup Script
echo "🚀 Setting up Resume Parser..."

# Check Python version
echo "Checking Python version..."
python3 --version

# Create virtual environment (optional but recommended)
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Download spaCy model
echo "Downloading spaCy English model..."
python -m spacy download en_core_web_sm

# Create uploads directory
echo "Creating uploads directory..."
mkdir -p uploads

echo "✅ Setup complete!"
echo ""
echo "To start the backend server, run:"
echo "  cd api"
echo "  uvicorn api:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "Then open web/index.html in your browser"
echo ""
echo "Happy parsing! 📄"
