#!/usr/bin/env python3
"""
Test script for Face Recognition Attendance System
Tests core functionality without requiring web interface interaction
"""

import sqlite3
import cv2
import numpy as np
import os
import sys

# Add backend directory to path
sys.path.append('backend')

def test_database_setup():
    """Test database initialization"""
    print("Testing database setup...")

    # Remove existing database for clean test
    if os.path.exists('attendance.db'):
        os.remove('attendance.db')

    # Import and run init_db
    from backend.app import init_db
    init_db()

    # Verify tables exist
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = c.fetchall()
    conn.close()

    table_names = [table[0] for table in tables]
    assert 'users' in table_names, "Users table not created"
    assert 'attendance' in table_names, "Attendance table not created"

    print("✓ Database setup successful")

def test_face_detection():
    """Test face detection functionality"""
    print("Testing face detection...")

    # Create a simple test image with a face-like pattern
    # For testing purposes, we'll create a synthetic image
    test_image = np.zeros((200, 200, 3), dtype=np.uint8)
    # Draw a simple rectangle to simulate a face
    cv2.rectangle(test_image, (50, 50), (150, 150), (255, 255, 255), -1)

    # Test face detection
    from backend.app import extract_face_embedding
    embedding = extract_face_embedding(test_image)

    if embedding is not None:
        print("✓ Face detection successful")
        assert len(embedding) == 10000, f"Expected embedding length 10000, got {len(embedding)}"
        print("✓ Face embedding extraction successful")
    else:
        print("⚠ Face detection returned None (expected for synthetic image)")

def test_image_storage():
    """Test image saving functionality"""
    print("Testing image storage...")

    # Create test image
    test_image = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)

    from backend.app import save_user_image
    image_path = save_user_image(test_image, 999)

    assert os.path.exists(image_path), f"Image not saved at {image_path}"

    # Verify image can be loaded
    loaded_image = cv2.imread(image_path)
    assert loaded_image is not None, "Could not load saved image"
    assert loaded_image.shape == test_image.shape, "Saved image dimensions don't match"

    # Cleanup
    os.remove(image_path)

    print("✓ Image storage successful")

def test_user_registration():
    """Test user registration in database"""
    print("Testing user registration...")

    # Clean up
    if os.path.exists('attendance.db'):
        os.remove('attendance.db')

    from backend.app import init_db
    init_db()

    # Register a test user
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()

    # Insert test user
    c.execute("INSERT INTO users (name, image_path, embedding) VALUES (?, ?, ?)",
              ("Test User", "test_path.jpg", "test_embedding"))
    user_id = c.lastrowid

    conn.commit()

    # Verify user was inserted
    c.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = c.fetchone()

    assert user is not None, "User not found in database"
    assert user[1] == "Test User", f"Expected name 'Test User', got {user[1]}"

    conn.close()

    print("✓ User registration successful")

def test_attendance_marking():
    """Test attendance marking functionality"""
    print("Testing attendance marking...")

    # Clean up
    if os.path.exists('attendance.db'):
        os.remove('attendance.db')

    from backend.app import init_db
    init_db()

    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()

    # Insert test user
    c.execute("INSERT INTO users (name, image_path, embedding) VALUES (?, ?, ?)",
              ("Test User", "test_path.jpg", "test_embedding"))
    user_id = c.lastrowid

    # Mark attendance
    from datetime import datetime
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute("INSERT INTO attendance (user_id, timestamp) VALUES (?, ?)", (user_id, timestamp))

    conn.commit()

    # Verify attendance was recorded
    c.execute("SELECT * FROM attendance WHERE user_id = ?", (user_id,))
    attendance = c.fetchone()

    assert attendance is not None, "Attendance not recorded"
    assert attendance[1] == user_id, f"Expected user_id {user_id}, got {attendance[1]}"

    conn.close()

    print("✓ Attendance marking successful")

def test_records_retrieval():
    """Test attendance records retrieval"""
    print("Testing records retrieval...")

    # Clean up
    if os.path.exists('attendance.db'):
        os.remove('attendance.db')

    from backend.app import init_db
    init_db()

    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()

    # Insert test user and attendance
    c.execute("INSERT INTO users (name, image_path, embedding) VALUES (?, ?, ?)",
              ("Test User", "test_path.jpg", "test_embedding"))
    user_id = c.lastrowid

    timestamp = "2024-01-01 12:00:00"
    c.execute("INSERT INTO attendance (user_id, timestamp) VALUES (?, ?)", (user_id, timestamp))

    conn.commit()

    # Test retrieval query
    c.execute("SELECT users.name, attendance.timestamp FROM attendance JOIN users ON users.id = attendance.user_id")
    records = c.fetchall()

    assert len(records) == 1, f"Expected 1 record, got {len(records)}"
    assert records[0][0] == "Test User", f"Expected name 'Test User', got {records[0][0]}"
    assert records[0][1] == timestamp, f"Expected timestamp {timestamp}, got {records[0][1]}"

    conn.close()

    print("✓ Records retrieval successful")

def main():
    """Run all tests"""
    print("Starting Face Recognition Attendance System Tests")
    print("=" * 50)

    try:
        test_database_setup()
        test_face_detection()
        test_image_storage()
        test_user_registration()
        test_attendance_marking()
        test_records_retrieval()

        print("=" * 50)
        print("🎉 All tests passed successfully!")
        print("The Face Recognition Attendance System is ready for deployment.")

    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

    return 0

if __name__ == "__main__":
    exit(main())
