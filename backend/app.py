import streamlit as st
import sqlite3
from deepface import DeepFace
import cv2
import numpy as np
from datetime import datetime
import pandas as pd
import os

# Database setup
def init_db():
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    image_path TEXT NOT NULL
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS attendance (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER,
                    timestamp TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )''')
    conn.commit()
    conn.close()

# Create images directory
if not os.path.exists('user_images'):
    os.makedirs('user_images')

init_db()

# Helper functions
def save_user_image(image, user_id):
    image_path = f"user_images/user_{user_id}.jpg"
    cv2.imwrite(image_path, image)
    return image_path

# Streamlit app
st.title("Face Recognition Attendance System")

# Sidebar navigation
page = st.sidebar.selectbox("Choose a page", ["Admin Login", "Register", "Attendance", "Records"])

if page == "Admin Login":
    st.header("Admin Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == 'admin' and password == 'admin123':
            st.success("Logged in successfully")
            st.session_state.logged_in = True
        else:
            st.error("Invalid Credentials")

elif page == "Register":
    if st.session_state.get('logged_in', False):
        st.header("Register New User")
        name = st.text_input("Enter Name")
        uploaded_file = st.camera_input("Take a photo") or st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

        if st.button("Register"):
            if name and uploaded_file:
                # Convert uploaded file to numpy array
                file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
                image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

                # Check if face is detected
                try:
                    faces = DeepFace.extract_faces(img_path=image, enforce_detection=True)
                    if faces:
                        # Save user to database
                        conn = sqlite3.connect('attendance.db')
                        c = conn.cursor()
                        c.execute("INSERT INTO users (name, image_path) VALUES (?, ?)", (name, "temp"))
                        user_id = c.lastrowid

                        # Save image
                        image_path = save_user_image(image, user_id)
                        c.execute("UPDATE users SET image_path = ? WHERE id = ?", (image_path, user_id))

                        conn.commit()
                        conn.close()

                        st.success("User registered successfully")
                    else:
                        st.error("No face detected")
                except Exception as e:
                    st.error(f"Face detection error: {str(e)}")
            else:
                st.error("Please enter name and provide an image")
    else:
        st.error("Please login as admin first")

elif page == "Attendance":
    if st.session_state.get('logged_in', False):
        st.header("Mark Attendance")
        uploaded_file = st.camera_input("Take a photo") or st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

        if st.button("Mark Attendance"):
            if uploaded_file:
                image = face_recognition.load_image_file(uploaded_file)
                encodings = face_recognition.face_encodings(image)

                if not encodings:
                    st.error("No face found")
                else:
                    face_encoding = encodings[0]

                    conn = sqlite3.connect('attendance.db')
                    c = conn.cursor()
                    c.execute("SELECT id, name, encoding FROM users")
                    users = c.fetchall()

                    known_encodings = [decode_face(user[2]) for user in users]

                    matches = face_recognition.compare_faces(known_encodings, face_encoding)

                    if True in matches:
                        user_id = users[matches.index(True)][0]
                        now = datetime.now()
                        timestamp = now.strftime('%Y-%m-%d %H:%M:%S')

                        c.execute("INSERT INTO attendance (user_id, timestamp) VALUES (?, ?)", (user_id, timestamp))
                        conn.commit()
                        conn.close()

                        st.success("Attendance marked")
                    else:
                        st.error("Face not recognized")
            else:
                st.error("Please provide an image")
    else:
        st.error("Please login as admin first")

elif page == "Records":
    if st.session_state.get('logged_in', False):
        st.header("Attendance Records")
        conn = sqlite3.connect('attendance.db')
        c = conn.cursor()
        c.execute("SELECT users.name, attendance.timestamp FROM attendance JOIN users ON users.id = attendance.user_id")
        data = c.fetchall()
        conn.close()

        if data:
            df = pd.DataFrame(data, columns=["Name", "Timestamp"])
            st.dataframe(df)
        else:
            st.info("No records found")
    else:
        st.error("Please login as admin first")

st.markdown("---")
st.markdown("Made with ❤️ from Sohel")
