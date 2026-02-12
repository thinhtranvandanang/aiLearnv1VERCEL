#!/usr/bin/env python3
"""
Check available questions in database
"""

import psycopg2

# Database configuration
DATABASE_URL = "postgresql://edunexia_user:123456@localhost:5432/edunexia_dev"

def check_questions():
    """Check available questions in database"""
    
    try:
        # Connect to database
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        # Check available questions
        cursor.execute("SELECT DISTINCT subject, topic, level FROM questions ORDER BY subject, topic, level")
        questions = cursor.fetchall()
        
        print("📋 Available questions:")
        for row in questions:
            print(f"  {row[0]} - {row[1]} - {row[2]}")
        
        # Count total questions
        cursor.execute("SELECT COUNT(*) FROM questions")
        total = cursor.fetchone()[0]
        print(f"\n📊 Total questions: {total}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    check_questions()
