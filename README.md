# Face Recognition Attendance System

A Streamlit-based face recognition attendance system with admin login, user registration, and attendance tracking.

## 🚀 Quick Start from GitHub

### Prerequisites
- Python 3.7 or higher
- Git
- pip (Python package installer)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd face-recognition-attendance/backend
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

   Or if `streamlit` command is not found:
   ```bash
   python -m streamlit run app.py
   ```

4. **Access the application**
   Open your browser and go to: `http://localhost:8501`

## 📁 Project Structure

```
face-recognition-attendance/
├── backend/
│   ├── app.py                    # Main Streamlit application
│   ├── requirements.txt          # Python dependencies
│   ├── haarcascade_frontalface_default.xml  # Face detection model
│   └── attendance.db             # SQLite database (auto-created)
├── frontend/                     # React frontend (optional)
├── user_images/                  # User image storage
├── README.md                     # This file
└── TODO.md                       # Project tasks
```

## 🔧 Features

- **Admin Login**: Username: `admin`, Password: `admin123`
- **User Registration**: Register new users with face capture
- **Attendance Marking**: Mark attendance using face recognition
- **Records View**: View all attendance records
- **Face Recognition**: Uses OpenCV with Haar Cascades for face detection

## 🛠️ Troubleshooting

### Common Issues and Solutions

1. **"streamlit: command not found"**
   ```bash
   # Try using python module approach
   python -m streamlit run app.py
   
   # Or reinstall streamlit
   pip install streamlit
   ```

2. **Permission errors during installation**
   ```bash
   # Use user installation
   pip install --user -r requirements.txt
   ```

3. **OpenCV installation issues**
   ```bash
   # For macOS with Apple Silicon
   pip install opencv-python
   
   # For other systems
   pip install opencv-python-headless
   ```

4. **Port already in use**
   ```bash
   # Use a different port
   streamlit run app.py --server.port 8502
   ```

5. **Face detection not working**
   - Ensure good lighting conditions
   - Face should be clearly visible
   - Try different angles and distances

### Camera Permissions (macOS)

If camera access is denied:
1. Go to System Preferences > Security & Privacy > Privacy
2. Select Camera
3. Enable access for Terminal or your Python application

### Database Issues

The SQLite database is automatically created. If you need to reset:
```bash
rm attendance.db
# Restart the application - database will be recreated
```

## 🔐 Default Admin Credentials

- **Username**: `admin`
- **Password**: `admin123`

## 📝 Usage Guide

1. **Login**: Use admin credentials to access the system
2. **Register Users**: Add new users by capturing their face
3. **Mark Attendance**: Use face recognition to mark attendance
4. **View Records**: Check all attendance records in table format

## 🏃‍♂️ Automated Setup Script

Use the provided setup script for quick installation:

```bash
chmod +x setup.sh
./setup.sh
```

## 🐛 Development

### Running in Development Mode

```bash
# Enable auto-reload
export STREAMLIT_SERVER_ENABLE_CORS=false
export STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false
streamlit run app.py
```

### Database Schema

**Users Table**:
- `id` (INTEGER PRIMARY KEY)
- `name` (TEXT NOT NULL)
- `image_path` (TEXT NOT NULL)
- `embedding` (TEXT NOT NULL)

**Attendance Table**:
- `id` (INTEGER PRIMARY KEY)
- `user_id` (INTEGER, FOREIGN KEY)
- `timestamp` (TEXT)

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📞 Support

If you encounter any issues, please check the troubleshooting section above or create an issue in the repository.

---

**Made with ❤️ from Sohel**
