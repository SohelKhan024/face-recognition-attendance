# Manual Deployment Guide - Streamlit from GitHub

## 🚀 Deploy Streamlit App Manually from GitHub Repository

This guide shows you exactly how to deploy your Streamlit face recognition attendance system from the GitHub repository manually.

## 📋 Prerequisites

Before starting, ensure you have:
- Python 3.7 or higher installed
- pip (Python package manager)
- Git installed
- Web browser with camera access

## 🎯 Step-by-Step Manual Deployment

### Step 1: Clone the Repository
```bash
# Clone your GitHub repository
git clone https://github.com/SohelKhan024/face-recognition-attendance.git

# Navigate to the project directory
cd face-recognition-attendance

# Navigate to the backend folder (where the Streamlit app is)
cd backend
```

### Step 2: Set Up Virtual Environment (Recommended)
```bash
# Create a virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
# Install all required packages
pip install -r requirements.txt

# If you encounter permission issues, try:
pip install --user -r requirements.txt
```

### Step 4: Verify Installation
```bash
# Check if streamlit is installed
python -c "import streamlit; print('Streamlit version:', streamlit.__version__)"

# Check if opencv is installed
python -c "import cv2; print('OpenCV version:', cv2.__version__)"
```

### Step 5: Run the Streamlit Application
```bash
# Method 1: Using streamlit command
streamlit run app.py

# Method 2: If streamlit command not found, use python module
python -m streamlit run app.py

# Method 3: Specify custom port
python -m streamlit run app.py --server.port 8501
```

### Step 6: Access Your Application
1. Open your web browser
2. Navigate to: `http://localhost:8501`
3. Use admin credentials to login:
   - **Username**: `admin`
   - **Password**: `admin123`

## 🌐 Alternative Deployment Methods

### Method A: Direct Git Clone and Run
```bash
# One-liner for quick deployment
git clone https://github.com/SohelKhan024/face-recognition-attendance.git && cd face-recognition-attendance/backend && pip install -r requirements.txt && python -m streamlit run app.py
```

### Method B: Download ZIP from GitHub
1. Go to: https://github.com/SohelKhan024/face-recognition-attendance
2. Click "Code" → "Download ZIP"
3. Extract the ZIP file
4. Navigate to `backend` folder
5. Run: `pip install -r requirements.txt`
6. Run: `python -m streamlit run app.py`

## 🔧 Configuration Options

### Custom Port
```bash
python -m streamlit run app.py --server.port 8080
```

### Network Access (for remote access)
```bash
python -m streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

### Disable Auto-reload (for production)
```bash
python -m streamlit run app.py --server.enableCORS false --server.enableXsrfProtection false
```

## 🛠️ Troubleshooting Manual Deployment

### Issue 1: "streamlit: command not found"
**Solution:**
```bash
# Try using python module approach
python -m streamlit run app.py

# Or reinstall streamlit
pip install streamlit --upgrade
```

### Issue 2: "Permission denied" during pip install
**Solution:**
```bash
# Use user installation
pip install --user -r requirements.txt

# Or use virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### Issue 3: OpenCV installation fails
**Solution:**
```bash
# For headless systems
pip install opencv-python-headless

# For systems with GUI
pip install opencv-python
```

### Issue 4: Port 8501 already in use
**Solution:**
```bash
# Use a different port
python -m streamlit run app.py --server.port 8502

# Or find and kill the process using port 8501
# On Mac/Linux:
lsof -ti:8501 | xargs kill -9

# On Windows:
netstat -ano | findstr :8501
taskkill /PID <PID_NUMBER> /F
```

### Issue 5: Camera not working
**Solution:**
1. **Browser Permissions:**
   - Go to browser settings → Privacy → Camera
   - Allow camera access for localhost

2. **System Permissions (macOS):**
   - System Preferences → Security & Privacy → Privacy → Camera
   - Enable access for Terminal or Python

3. **Test camera access:**
   ```python
   python -c "import cv2; cap = cv2.VideoCapture(0); print('Camera working:', cap.isOpened()); cap.release()"
   ```

## 📁 File Structure After Deployment
```
face-recognition-attendance/
├── backend/
│   ├── app.py                    # Main Streamlit application
│   ├── requirements.txt          # Dependencies
│   ├── haarcascade_frontalface_default.xml
│   ├── attendance.db             # Auto-created database
│   └── user_images/              # Auto-created user images folder
├── frontend/                     # React frontend (optional)
└── README.md                     # Documentation
```

## 🔐 Security Considerations

### For Production Deployment:
1. **Change admin credentials** in `app.py`
2. **Use HTTPS** in production
3. **Set up authentication** beyond simple username/password
4. **Restrict network access** if not needed
5. **Regular backups** of the database

### Environment Variables:
```bash
# Set environment variables for security
export STREAMLIT_SERVER_ENABLE_CORS=false
export STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=true
python -m streamlit run app.py
```

## 📊 Performance Optimization

### For Better Performance:
```bash
# Install watchdog for faster file watching
pip install watchdog

# Enable caching
python -m streamlit run app.py --server.enableCaching true

# Optimize memory usage
python -m streamlit run app.py --server.maxMessageSize 200
```

## 🚀 Deployment on Different Platforms

### Windows:
```cmd
# Use Command Prompt or PowerShell
git clone https://github.com/SohelKhan024/face-recognition-attendance.git
cd face-recognition-attendance\backend
pip install -r requirements.txt
python -m streamlit run app.py
```

### macOS:
```bash
# Use Terminal
git clone https://github.com/SohelKhan024/face-recognition-attendance.git
cd face-recognition-attendance/backend
pip3 install -r requirements.txt
python3 -m streamlit run app.py
```

### Linux (Ubuntu/Debian):
```bash
# Install system dependencies first
sudo apt update
sudo apt install python3 python3-pip git

# Then deploy
git clone https://github.com/SohelKhan024/face-recognition-attendance.git
cd face-recognition-attendance/backend
pip3 install -r requirements.txt
python3 -m streamlit run app.py
```

## 🔄 Updating the Deployment

To update your deployed app:
```bash
# Navigate to project directory
cd face-recognition-attendance

# Pull latest changes from GitHub
git pull origin main

# Navigate to backend and update dependencies if needed
cd backend
pip install -r requirements.txt --upgrade

# Restart the application
python -m streamlit run app.py
```

## 📱 Access URLs

### Local Access:
- **Main App**: http://localhost:8501
- **Alternative Port**: http://localhost:8502 (if using custom port)

### Network Access:
- **LAN Access**: http://YOUR_LOCAL_IP:8501
- **Find your IP**: 
  - Windows: `ipconfig`
  - Mac/Linux: `ifconfig` or `ip addr`

## 🎉 Success Verification

Your deployment is successful when:
1. ✅ No error messages in terminal
2. ✅ Streamlit shows "You can now view your Streamlit app in your browser"
3. ✅ App loads at http://localhost:8501
4. ✅ Admin login works (admin/admin123)
5. ✅ Camera access is granted
6. ✅ Face detection works for registration

---

**🎯 Your Streamlit face recognition attendance system is now manually deployed and ready to use!**

Made with ❤️ from Sohel
