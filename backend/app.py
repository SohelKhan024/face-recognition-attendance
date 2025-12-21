import streamlit as st
import sqlite3
import cv2
import numpy as np
from datetime import datetime
import pandas as pd
import os
import urllib.request

# Download Haar cascade if not present
if not os.path.exists('haarcascade_frontalface_default.xml'):
    try:
        urllib.request.urlretrieve('https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml', 'haarcascade_frontalface_default.xml')
    except:
        pass  # Continue if download fails

# Database setup
def init_db():
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    image_path TEXT NOT NULL,
                    embedding TEXT NOT NULL
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

def extract_face_embedding(image):
    """Extract face embedding using OpenCV and basic image processing"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Use Haar cascade for face detection
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    if len(faces) == 0:
        return None

    # Take the first face found
    x, y, w, h = faces[0]
    face = gray[y:y+h, x:x+w]

    # Resize to standard size
    face_resized = cv2.resize(face, (100, 100))

    # Flatten to create a simple embedding
    embedding = face_resized.flatten().astype(np.float32)
    embedding = embedding / np.linalg.norm(embedding)  # Normalize

    return embedding

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

                # Check if face is detected and extract embedding
                try:
                    embedding = extract_face_embedding(image)
                    if embedding is not None:
                        # Save user to database
                        conn = sqlite3.connect('attendance.db')
                        c = conn.cursor()

                        # Save image first
                        image_path = save_user_image(image, 0)  # Temporary ID
                        embedding_str = ','.join(map(str, embedding.tolist()))

                        c.execute("INSERT INTO users (name, image_path, embedding) VALUES (?, ?, ?)",
                                (name, image_path, embedding_str))
                        user_id = c.lastrowid

                        # Update image path with correct user ID
                        correct_image_path = save_user_image(image, user_id)
                        c.execute("UPDATE users SET image_path = ? WHERE id = ?", (correct_image_path, user_id))

                        # Remove temporary image
                        if os.path.exists(image_path):
                            os.remove(image_path)

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
                # Convert uploaded file to numpy array
                file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
                image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

                # Check if face is detected and recognize user
                try:
                    current_embedding = extract_face_embedding(image)
                    if current_embedding is not None:
                        # Get all registered users
                        conn = sqlite3.connect('attendance.db')
                        c = conn.cursor()
                        c.execute("SELECT id, name, embedding FROM users")
                        users = c.fetchall()
                        conn.close()

                        if not users:
                            st.error("No registered users found")

                        # Try to match against each user using cosine similarity
                        recognized_user = None
                        best_similarity = 0.0

                        for user_id, name, embedding_str in users:
                            try:
                                stored_embedding = np.array([float(x) for x in embedding_str.split(',')])
                                similarity = np.dot(current_embedding, stored_embedding) / (
                                    np.linalg.norm(current_embedding) * np.linalg.norm(stored_embedding)
                                )

                                if similarity > 0.8 and similarity > best_similarity:  # Threshold for recognition
                                    recognized_user = (user_id, name)
                                    best_similarity = similarity
                            except Exception:
                                continue

                        if recognized_user:
                            user_id, name = recognized_user
                            now = datetime.now()
                            timestamp = now.strftime('%Y-%m-%d %H:%M:%S')

                            conn = sqlite3.connect('attendance.db')
                            c = conn.cursor()
                            c.execute("INSERT INTO attendance (user_id, timestamp) VALUES (?, ?)", (user_id, timestamp))
                            conn.commit()
                            conn.close()

                            st.success(f"Attendance marked for {name}")
                        else:
                            st.error("Face not recognized")
                    else:
                        st.error("No face found")
                except Exception as e:
                    st.error(f"Face detection error: {str(e)}")
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
