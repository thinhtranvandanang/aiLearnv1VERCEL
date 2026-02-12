#!/usr/bin/env python3
"""
Add more questions to database to support larger question_count requests
"""

import psycopg2
import json

# Database configuration
DATABASE_URL = "postgresql://edunexia_user:123456@localhost:5432/edunexia_dev"

def add_more_questions():
    """Add more questions to each subject-topic-level combination"""
    
    try:
        # Connect to database
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        # Additional questions for each combination
        additional_questions = [
            # Math - Đạo hàm - Easy (add 2 more)
            ("Toán học", "Đạo hàm", "easy", "Tìm đạo hàm của hàm số f(x) = x³ - 2x² + 5x - 1", 
             json.dumps({"A": "f'(x) = 3x² - 4x + 5", "B": "f'(x) = 3x² - 4x", "C": "f'(x) = x² - 2x + 5", "D": "f'(x) = 3x² + 5"}), 
             "A", "Đạo hàm của x³ là 3x², của -2x² là -4x, của 5x là 5, của -1 là 0. Vậy f'(x) = 3x² - 4x + 5"),
            
            ("Toán học", "Đạo hàm", "easy", "Tìm đạo hàm của hàm số f(x) = √x + 1/x", 
             json.dumps({"A": "f'(x) = 1/(2√x) - 1/x²", "B": "f'(x) = 1/(2√x) + 1/x²", "C": "f'(x) = 2√x - 1/x²", "D": "f'(x) = 1/(2√x) - x"}), 
             "A", "Đạo hàm của √x = x^(1/2) là (1/2)x^(-1/2) = 1/(2√x). Đạo hàm của 1/x = x^(-1) là -x^(-2) = -1/x²"),
            
            # Math - Đạo hàm - Medium (add 2 more)
            ("Toán học", "Đạo hàm", "medium", "Tìm đạo hàm của hàm số f(x) = ln(x² + 1)", 
             json.dumps({"A": "f'(x) = 2x/(x² + 1)", "B": "f'(x) = 1/(x² + 1)", "C": "f'(x) = 2x", "D": "f'(x) = x/(x² + 1)"}), 
             "A", "Sử dụng quy tắc chuỗi: (ln u)' = u'/u. Với u = x² + 1, u' = 2x. Vậy f'(x) = 2x/(x² + 1)"),
            
            ("Toán học", "Đạo hàm", "medium", "Tìm đạo hàm của hàm số f(x) = cos²(x)", 
             json.dumps({"A": "f'(x) = -2cos(x)sin(x)", "B": "f'(x) = 2cos(x)sin(x)", "C": "f'(x) = -sin²(x)", "D": "f'(x) = cos(2x)"}), 
             "A", "Sử dụng quy tắc chuỗi: (u²)' = 2u*u'. Với u = cos(x), u' = -sin(x). Vậy f'(x) = 2cos(x)*(-sin(x)) = -2cos(x)sin(x)"),
            
            # Physics - Sóng cơ - Easy (add 2 more)
            ("Vật lý", "Sóng cơ", "easy", "Đặc điểm nào sau đây đúng về sóng cơ?", 
             json.dumps({"A": "Cần môi trường để truyền", "B": "Có thể truyền trong chân không", "C": "Tốc độ không phụ thuộc môi trường", "D": "Chỉ truyền theo phương thẳng đứng"}), 
             "A", "Sóng cơ là sóng cơ học, cần môi trường vật chất đàn hồi để truyền năng lượng"),
            
            ("Vật lý", "Sóng cơ", "easy", "Sóng ngang là sóng có:", 
             json.dumps({"A": "Hạt vật chất dao động vuông góc với phương truyền sóng", "B": "Hạt vật chất dao động cùng phương với phương truyền sóng", "C": "Hạt vật chất không dao động", "D": "Hạt vật chất dao động theo đường tròn"}), 
             "A", "Định nghĩa: Sóng ngang là sóng mà các hạt vật chất dao động vuông góc với phương truyền của sóng"),
            
            # Physics - Sóng cơ - Medium (add 2 more)
            ("Vật lý", "Sóng cơ", "medium", "Tần số và chu kỳ của sóng có mối quan hệ:", 
             json.dumps({"A": "T = 1/f", "B": "T = f", "C": "T = f²", "D": "T = 2πf"}), 
             "A", "Tần số f và chu kỳ T có mối quan hệ nghịch đảo: T = 1/f hoặc f = 1/T"),
            
            ("Vật lý", "Sóng cơ", "medium", "Biên độ của sóng là:", 
             json.dumps({"A": "Độ lớn nhất của dao động", "B": "Tốc độ truyền sóng", "C": "Số dao động trong 1 giây", "D": "Khoảng cách giữa hai đỉnh sóng liên tiếp"}), 
             "A", "Biên độ A là độ lớn nhất của dao động, thể hiện cường độ năng lượng của sóng"),
            
            # Chemistry - Phản ứng oxi-hóa khử - Easy (add 2 more)
            ("Hóa học", "Phản ứng oxi-hóa khử", "easy", "Trong phản ứng: Cu + 2Ag⁺ → Cu²⁺ + 2Ag. Chất khử là gì?", 
             json.dumps({"A": "Cu", "B": "Ag⁺", "C": "Cu²⁺", "D": "Ag"}), 
             "A", "Cu có số oxi hóa tăng từ 0 → +2, nên Cu bị oxi hóa, là chất khử"),
            
            ("Hóa học", "Phản ứng oxi-hóa khử", "easy", "Phản ứng nào sau đây không phải là phản ứng oxi-hóa khử?", 
             json.dumps({"A": "2H₂ + O₂ → 2H₂O", "B": "NaCl + AgNO₃ → AgCl + NaNO₃", "C": "Fe + CuSO₄ → FeSO₄ + Cu", "D": "2Mg + O₂ → 2MgO"}), 
             "B", "Phản ứng trao đổi ion NaCl + AgNO₃ → AgCl + NaNO₃ không có sự thay đổi số oxi hóa"),
            
            # English - Câu bị động - Easy (add 2 more)
            ("Tiếng Anh", "Câu bị động", "easy", "Chuyển câu sau sang bị động: 'She writes a letter every day.'", 
             json.dumps({"A": "A letter is written by her every day.", "B": "A letter was written by her every day.", "C": "A letter writes by her every day.", "D": "A letter is wrote by her every day."}), 
             "A", "Câu bị động ở thì hiện tại đơn: S + is/are + V3 + (by O). 'writes' → 'is written'"),
            
            ("Tiếng Anh", "Câu bị động", "easy", "Chuyển câu sau sang bị động: 'They clean the room daily.'", 
             json.dumps({"A": "The room is cleaned daily.", "B": "The room was cleaned daily.", "C": "The room cleans daily.", "D": "The room is cleaning daily."}), 
             "A", "Câu bị động ở thì hiện tại đơn: 'clean' → 'is cleaned'")
        ]
        
        # Insert questions
        insert_query = """
        INSERT INTO questions (subject, topic, level, content, options, correct_answer, explanation, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
        """
        
        cursor.executemany(insert_query, additional_questions)
        conn.commit()
        
        print(f"✅ Successfully added {len(additional_questions)} more questions")
        
        # Verify new counts
        cursor.execute("SELECT subject, topic, level, COUNT(*) FROM questions GROUP BY subject, topic, level ORDER BY subject, topic, level")
        print("\n📊 Updated question counts:")
        for row in cursor.fetchall():
            print(f"  {row[0]} - {row[1]} - {row[2]}: {row[3]} questions")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    add_more_questions()
