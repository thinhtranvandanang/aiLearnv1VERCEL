#!/usr/bin/env python3
"""
Seed production database with sample questions
Run this after database is created on Render
"""

import os
import psycopg2
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def seed_production_db():
    """Seed production database with sample data"""
    
    # Get database URL from environment
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL environment variable not found")
        return
    
    try:
        # Connect directly with psycopg2 for initial setup
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        print("🌱 Seeding production database...")
        
        # Sample questions for production
        questions = [
            # Math - Derivatives
            ("Toán học", "Đạo hàm", "easy", "Tìm đạo hàm của hàm số f(x) = 3x² + 2x - 5", 
             json.dumps({"A": "f'(x) = 6x + 2", "B": "f'(x) = 3x + 2", "C": "f'(x) = 6x - 2", "D": "f'(x) = 3x² + 2"}), 
             "A", "Đạo hàm của 3x² là 6x, của 2x là 2, của -5 là 0. Vậy f'(x) = 6x + 2"),
            
            ("Toán học", "Đạo hàm", "easy", "Tìm đạo hàm của hàm số f(x) = √x + 1/x", 
             json.dumps({"A": "f'(x) = 1/(2√x) - 1/x²", "B": "f'(x) = 1/(2√x) + 1/x²", "C": "f'(x) = 2√x - 1/x²", "D": "f'(x) = 1/(2√x) - x"}), 
             "A", "Đạo hàm của √x = x^(1/2) là (1/2)x^(-1/2) = 1/(2√x). Đạo hàm của 1/x = x^(-1) là -x^(-2) = -1/x²"),
            
            # Physics - Mechanical Waves
            ("Vật lý", "Sóng cơ", "easy", "Đặc điểm nào sau đây đúng về sóng cơ?", 
             json.dumps({"A": "Cần môi trường để truyền", "B": "Có thể truyền trong chân không", "C": "Tốc độ không phụ thuộc môi trường", "D": "Chỉ truyền theo phương thẳng đứng"}), 
             "A", "Sóng cơ là sóng cơ học, cần môi trường vật chất đàn hồi để truyền năng lượng"),
            
            ("Vật lý", "Sóng cơ", "easy", "Sóng ngang là sóng có:", 
             json.dumps({"A": "Hạt vật chất dao động vuông góc với phương truyền sóng", "B": "Hạt vật chất dao động cùng phương với phương truyền sóng", "C": "Hạt vật chất không dao động", "D": "Hạt vật chất dao động theo đường tròn"}), 
             "A", "Định nghĩa: Sóng ngang là sóng mà các hạt vật chất dao động vuông góc với phương truyền của sóng"),
            
            # Chemistry - Redox Reactions
            ("Hóa học", "Phản ứng oxi-hóa khử", "easy", "Phản ứng nào sau đây là phản ứng oxi-hóa khử?", 
             json.dumps({"A": "NaOH + HCl → NaCl + H₂O", "B": "Zn + H₂SO₄ → ZnSO₄ + H₂", "C": "CaCO₃ → CaO + CO₂", "D": "HCl + NH₃ → NH₄Cl"}), 
             "B", "Trong phản ứng B, kẽm (Zn) bị oxi hóa từ 0 → +2, hydro (H) bị khử từ +1 → 0. Đây là phản ứng oxi-hóa khử"),
            
            # English - Passive Voice
            ("Tiếng Anh", "Câu bị động", "easy", "Chuyển câu sau sang bị động: 'She writes a letter every day.'", 
             json.dumps({"A": "A letter is written by her every day.", "B": "A letter was written by her every day.", "C": "A letter writes by her every day.", "D": "A letter is wrote by her every day."}), 
             "A", "Câu bị động ở thì hiện tại đơn: S + is/are + V3 + (by O). 'writes' → 'is written'"),
        ]
        
        # Insert questions
        insert_query = """
        INSERT INTO questions (subject, topic, level, content, options, correct_answer, explanation, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, NOW(), NOW())
        """
        
        cursor.executemany(insert_query, questions)
        conn.commit()
        
        print(f"✅ Successfully seeded {len(questions)} questions")
        
        # Verify
        cursor.execute("SELECT COUNT(*) FROM questions")
        total = cursor.fetchone()[0]
        print(f"📊 Total questions in database: {total}")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    seed_production_db()
