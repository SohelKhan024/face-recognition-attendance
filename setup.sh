#!/bin/bash

# Face Recognition Attendance System - Quick Setup Script
# Made with ❤️ from Sohel

echo "🚀 Setting up Face Recognition Attendance System..."
echo "=================================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7+ first."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Navigate to backend directory
cd backend || { echo "❌ Backend directory not found!"; exit 1; }

echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "⚠️  Installation had issues, trying with --user flag..."
    pip3 install --user -r requirements.txt
fi

echo "🎯 Starting Streamlit application..."
echo "📱 The app will be available at: http://localhost:8501"
echo "🔑 Admin Login - Username: admin, Password: admin123"
echo ""
echo "Press Ctrl+C to stop the application"
echo "=================================================="

# Start Streamlit
python3 -m streamlit run app.py --server.port 8501 --server.address 0.0.0.0
