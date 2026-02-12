#!/usr/bin/env python3
"""
Check and create a test user
"""

import psycopg2
import hashlib
from datetime import datetime

# Database configuration
DATABASE_URL = "postgresql://edunexia_user:123456@localhost:5432/edunexia_dev"

def check_and_create_user():
    """Check existing users and create a test user if needed"""
    
    try:
        # Connect to database
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        # Check existing users
        cursor.execute("SELECT id, username, email, role FROM users")
        users = cursor.fetchall()
        
        if users:
            print("📋 Existing users:")
            for user in users:
                print(f"   ID: {user[0]}, Username: {user[1]}, Email: {user[2]}, Role: {user[3]}")
        else:
            print("❌ No users found in database")
            
            # Create a test user
            print("🔧 Creating a test user...")
            
            # Hash password (simple approach for testing)
            password = "test123"
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            
            insert_query = """
            INSERT INTO users (username, email, hashed_password, full_name, role, is_active, is_locked, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
            RETURNING id
            """
            
            cursor.execute(insert_query, (
                "teststudent",
                "test@example.com", 
                hashed_password,
                "Test Student",
                "student",
                True,
                False
            ))
            
            user_id = cursor.fetchone()[0]
            conn.commit()
            
            print(f"✅ Created test user with ID: {user_id}")
            print(f"   Username: teststudent")
            print(f"   Password: test123")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    check_and_create_user()
