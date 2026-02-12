#!/usr/bin/env python3
"""
Check available topics in database
"""

import psycopg2

# Database configuration
DATABASE_URL = "postgresql://edunexia_user:123456@localhost:5432/edunexia_dev"

def check_topics():
    """Check available topics in database"""
    
    try:
        # Connect to database
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        # Check available topics
        cursor.execute("SELECT DISTINCT topic FROM questions ORDER BY topic")
        topics = cursor.fetchall()
        
        print("📋 Available topics in database:")
        for row in topics:
            print(f'  "{row[0]}"')
        
        # Check specific case
        cursor.execute("SELECT COUNT(*) FROM questions WHERE subject = 'Toán học' AND topic = 'đạo hàm' AND level = 'easy'")
        count_no_diacritics = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM questions WHERE subject = 'Toán học' AND topic = 'Đạo hàm' AND level = 'easy'")
        count_with_diacritics = cursor.fetchone()[0]
        
        print(f"\n🔍 Topic comparison:")
        print(f"  'đạo hàm' (no diacritics): {count_no_diacritics} questions")
        print(f"  'Đạo hàm' (with diacritics): {count_with_diacritics} questions")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    check_topics()
