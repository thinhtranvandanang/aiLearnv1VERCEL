#!/usr/bin/env python3
"""
Simple script to add sample questions directly to database
"""

import psycopg2

# Database configuration
DATABASE_URL = "postgresql://edunexia_user:123456@localhost:5432/edunexia_dev"

def add_questions():
    """Add sample questions to the database"""
    
    try:
        # Connect to database
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        # Check if questions already exist
        cursor.execute("SELECT COUNT(*) FROM questions")
        existing_count = cursor.fetchone()[0]
        
        if existing_count > 0:
            print(f"ℹ️  Database already has {existing_count} questions. Skipping seeding.")
            return
        
        # Sample questions
        questions = [
            # Math questions
            ("Toán học", "Đạo hàm", "easy", "Tìm đạo hàm của hàm số f(x) = 3x² + 2x - 5", 
             '{"A": "f(x) = 6x + 2", "B": "f(x) = 3x + 2", "C": "f(x) = 6x - 2", "D": "f(x) = 3x² + 2"}', 
             "A", "Đạo hàm của 3x² là 6x, đạo hàm của 2x là 2, đạo hàm của -5 là 0. Vậy f(x) = 6x + 2"),
            
            ("Toán học", "Đạo hàm", "medium", "Tìm đạo hàm của hàm số f(x) = sin(2x) + cos(3x)", 
             '{"A": "f(x) = 2cos(2x) - 3sin(3x)", "B": "f(x) = cos(2x) - sin(3x)", "C": "f(x) = 2cos(2x) + 3sin(3x)", "D": "f(x) = -2cos(2x) - 3sin(3x)"}', 
             "A", "Đạo hàm của sin(2x) là 2cos(2x), đạo hàm của cos(3x) là -3sin(3x). Vậy f(x) = 2cos(2x) - 3sin(3x)"),
            
            ("Toán học", "Đạo hàm", "hard", "Tìm đạo hàm của hàm số f(x) = e^(x²) * ln(x)", 
             '{"A": "f(x) = e^(x²) * (2x * ln(x) + 1/x)", "B": "f(x) = e^(x²) * (2x * ln(x))", "C": "f(x) = e^(x²) * (ln(x) + 1/x)", "D": "f(x) = 2x * e^(x²) * ln(x)"}', 
             "A", "Sử dụng quy tắc tích: (uv) = u v + uv. Với u = e^(x²), u = 2x*e^(x²); v = ln(x), v = 1/x. Vậy f(x) = 2x*e^(x²)*ln(x) + e^(x²)*(1/x) = e^(x²)*(2x*ln(x) + 1/x)"),
            
            # Physics questions
            ("Vật lý", "Sóng cơ", "easy", "Sóng cơ là gì?", 
             '{"A": "Sự truyền dao động trong môi trường đàn hồi", "B": "Sự truyền ánh sáng trong chân không", "C": "Sự truyền điện tử trong kim loại", "D": "Sự truyền nhiệt trong chất rắn"}', 
             "A", "Sóng cơ là sự truyền dao động của các hạt vật chất trong môi trường đàn hồi mà không có sự truyền chuyển dịch của vật chất"),
            
            ("Vật lý", "Sóng cơ", "medium", "Phương trình sóng đang truyền trên dây có dạng y = 0.02sin(10πt - 2πx). Tần số của sóng là bao nhiêu?", 
             '{"A": "5 Hz", "B": "10 Hz", "C": "2π Hz", "D": "10π Hz"}', 
             "A", "Phương trình sóng tổng quát: y = A sin(ωt - kx). So sánh với y = 0.02sin(10πt - 2πx), ta có ω = 10π. Tần số f = ω/(2π) = 10π/(2π) = 5 Hz"),
            
            ("Vật lý", "Sóng cơ", "hard", "Một nguồn sóng có tần số 100 Hz phát sóng trong môi trường có tốc độ truyền 340 m/s. Bước sóng của sóng là bao nhiêu?", 
             '{"A": "3.4 m", "B": "34 m", "C": "0.34 m", "D": "340 m"}', 
             "A", "Bước sóng λ = v/f = 340/100 = 3.4 m"),
            
            # Chemistry questions
            ("Hóa học", "Phản ứng oxi-hóa khử", "easy", "Phản ứng nào sau đây là phản ứng oxi-hóa khử?", 
             '{"A": "NaOH + HCl → NaCl + H₂O", "B": "Zn + H₂SO₄ → ZnSO₄ + H₂", "C": "CaCO₃ → CaO + CO₂", "D": "HCl + NH₃ → NH₄Cl"}', 
             "B", "Trong phản ứng B, kẽm (Zn) bị oxi hóa từ 0 → +2, hydro (H) bị khử từ +1 → 0. Đây là phản ứng oxi-hóa khử"),
            
            ("Hóa học", "Phản ứng oxi-hóa khử", "medium", "Trong phản ứng: 2Fe + 3Cl₂ → 2FeCl₃. Chất oxi hóa là gì?", 
             '{"A": "Fe", "B": "Cl₂", "C": "FeCl₃", "D": "Cả Fe và Cl₂"}', 
             "B", "Cl₂ có số oxi hóa giảm từ 0 → -1, nên Cl₂ là chất oxi hóa. Fe có số oxi hóa tăng từ 0 → +3, nên Fe là chất khử"),
            
            ("Hóa học", "Phản ứng oxi-hóa khử", "hard", "Cân bằng phản ứng oxi-hóa khử sau đây trong môi trường axit: MnO₄⁻ + Fe²⁺ → Mn²⁺ + Fe³⁺", 
             '{"A": "MnO₄⁻ + 5Fe²⁺ + 8H⁺ → Mn²⁺ + 5Fe³⁺ + 4H₂O", "B": "MnO₄⁻ + Fe²⁺ + 8H⁺ → Mn²⁺ + Fe³⁺ + 4H₂O", "C": "MnO₄⁻ + 5Fe²⁺ + 4H⁺ → Mn²⁺ + 5Fe³⁺ + 2H₂O", "D": "2MnO₄⁻ + 5Fe²⁺ + 16H⁺ → 2Mn²⁺ + 5Fe³⁺ + 8H₂O"}', 
             "A", "Nửa phản ứng oxi hóa: Fe²⁺ → Fe³⁺ + e⁻ (nhân 5). Nửa phản ứng khử: MnO₄⁻ + 8H⁺ + 5e⁻ → Mn²⁺ + 4H₂O. Cộng lại ta được: MnO₄⁻ + 5Fe²⁺ + 8H⁺ → Mn²⁺ + 5Fe³⁺ + 4H₂O"),
            
            # English questions
            ("Tiếng Anh", "Câu bị động", "easy", "Chuyển câu sau sang bị động: 'They built this house last year.'", 
             '{"A": "This house was built last year.", "B": "This house is built last year.", "C": "This house built last year.", "D": "This house has been built last year."}', 
             "A", "Câu bị động ở thì quá khứ đơn: S + was/were + V3 + (by O). 'They built' → 'was built'"),
            
            ("Tiếng Anh", "Câu bị động", "medium", "Chuyển câu sau sang bị động: 'Someone is painting the room now.'", 
             '{"A": "The room is being painted now.", "B": "The room is painted now.", "C": "The room being painted now.", "D": "The room has been painted now."}', 
             "A", "Câu bị động ở thì hiện tại tiếp diễn: S + is/are + being + V3. 'is painting' → 'is being painted'"),
            
            ("Tiếng Anh", "Câu bị động", "hard", "Chuyển câu sau sang bị động: 'They will have completed the project by next month.'", 
             '{"A": "The project will have been completed by next month.", "B": "The project will be completed by next month.", "C": "The project will have completed by next month.", "D": "The project will have being completed by next month."}', 
             "A", "Câu bị động ở thì tương lai hoàn thành: S + will + have + been + V3. 'will have completed' → 'will have been completed'")
        ]
        
        # Insert questions
        insert_query = """
        INSERT INTO questions (subject, topic, level, content, options, correct_answer, explanation, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
        """
        
        cursor.executemany(insert_query, questions)
        conn.commit()
        
        print(f"✅ Successfully added {len(questions)} questions to the database")
        
        # Verify seeding
        cursor.execute("SELECT COUNT(*) FROM questions")
        total_questions = cursor.fetchone()[0]
        print(f"📊 Total questions in database: {total_questions}")
        
        # Show distribution
        cursor.execute("SELECT subject, COUNT(*) FROM questions GROUP BY subject")
        subjects = cursor.fetchall()
        for subject, count in subjects:
            print(f"   - {subject}: {count} questions")
            
    except Exception as e:
        print(f"❌ Error adding questions: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    add_questions()
