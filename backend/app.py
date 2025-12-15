import streamlit as st
import sqlite3
import face_recognition
import cv2
import numpy as np
from datetime import datetime
import pandas as pd

# Database setup
def init_db():
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    encoding TEXT NOT NULL
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS attendance (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER,
                    timestamp TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )''')
    conn.commit()
    conn.close()

init_db()

# Helper functions
def encode_face(image):
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_image)
    if face_locations:
        face_encoding = face_recognition.face_encodings(rgb_image, face_locations)[0]
        return face_encoding.tolist()
    return None

def decode_face(encoding_str):
    return np.array([float(x) for x in encoding_str.split(',')])

def recognize_face(image, known_encodings):
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_image)
    if face_locations:
        face_encoding = face_recognition.face_encodings(rgb_image, face_locations)[0]
        matches = face_recognition.compare_faces(known_encodings, face_encoding)
        if True in matches:
            return matches.index(True)
    return None

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
                image = face_recognition.load_image_file(uploaded_file)
                encodings = face_recognition.face_encodings(image)

                if not encodings:
                    st.error("No face detected")
                else:
                    encoding = encodings[0]
                    encoding_str = ','.join(map(str, encoding.tolist()))

                    conn = sqlite3.connect('attendance.db')
                    c = conn.cursor()
                    c.execute("INSERT INTO users (name, encoding) VALUES (?, ?)", (name, encoding_str))
                    conn.commit()
                    conn.close()

                    st.success("User registered successfully")
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
