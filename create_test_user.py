#!/usr/bin/env python3
"""
Create a test user with proper bcrypt password hashing
"""

import psycopg2
from passlib.context import CryptContext

# Database configuration
DATABASE_URL = "postgresql://edunexia_user:123456@localhost:5432/edunexia_dev"

def create_test_user():
    """Create a test user with proper bcrypt password"""
    
    try:
        # Connect to database
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        # Use bcrypt for password hashing
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        password = "test123"
        # Truncate password to 72 characters as required by bcrypt
        safe_password = password[:72] if password else ""
        hashed_password = pwd_context.hash(safe_password)
        
        print(f"🔧 Creating test user with bcrypt hash...")
        print(f"   Password: {password}")
        print(f"   Hash: {hashed_password}")
        
        # Delete existing test user if exists
        cursor.execute("DELETE FROM users WHERE username = 'teststudent'")
        
        # Create new test user
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
    create_test_user()
