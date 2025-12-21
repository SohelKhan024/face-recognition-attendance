@echo off
REM Face Recognition Attendance System - Windows Setup Script
REM Made with ❤️ from Sohel

echo 🚀 Setting up Face Recognition Attendance System...
echo ==================================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.7+ first.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python found
python --version

REM Navigate to backend directory
if not exist "backend" (
    echo ❌ Backend directory not found!
    pause
    exit /b 1
)

cd backend

echo 📦 Installing dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo ⚠️  Installation had issues, trying with --user flag...
    pip install --user -r requirements.txt
)

echo 🎯 Starting Streamlit application...
echo 📱 The app will be available at: http://localhost:8501
echo 🔑 Admin Login - Username: admin, Password: admin123
echo.
echo Press Ctrl+C to stop the application
echo ==================================================

REM Start Streamlit
python -m streamlit run app.py --server.port 8501 --server.address 0.0.0.0

pause
