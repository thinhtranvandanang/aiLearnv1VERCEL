#!/usr/bin/env python3
"""
Seed the database with sample questions for testing
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import json
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.question import Question

def seed_questions():
    """Seed the database with sample questions"""
    db = SessionLocal()
    
    sample_questions = [
        # Math questions
        {
            "subject": "Toán học",
            "topic": "Đạo hàm",
            "level": "easy",
            "content": "Tìm đạo hàm của hàm số f(x) = 3x² + 2x - 5",
            "options": json.dumps({"A": "f'(x) = 6x + 2", "B": "f'(x) = 3x + 2", "C": "f'(x) = 6x - 2", "D": "f'(x) = 3x² + 2"}),
            "correct_answer": "A",
            "explanation": "Đạo hàm của 3x² là 6x, đạo hàm của 2x là 2, đạo hàm của -5 là 0. Vậy f'(x) = 6x + 2"
        },
        {
            "subject": "Toán học",
            "topic": "Đạo hàm",
            "level": "medium",
            "content": "Tìm đạo hàm của hàm số f(x) = sin(2x) + cos(3x)",
            "options": json.dumps({"A": "f'(x) = 2cos(2x) - 3sin(3x)", "B": "f'(x) = cos(2x) - sin(3x)", "C": "f'(x) = 2cos(2x) + 3sin(3x)", "D": "f'(x) = -2cos(2x) - 3sin(3x)"}),
            "correct_answer": "A",
            "explanation": "Đạo hàm của sin(2x) là 2cos(2x), đạo hàm của cos(3x) là -3sin(3x). Vậy f'(x) = 2cos(2x) - 3sin(3x)"
        },
        {
            "subject": "Toán học",
            "topic": "Đạo hàm",
            "level": "hard",
            "content": "Tìm đạo hàm của hàm số f(x) = e^(x²) * ln(x)",
            "options": json.dumps({"A": "f'(x) = e^(x²) * (2x * ln(x) + 1/x)", "B": "f'(x) = e^(x²) * (2x * ln(x))", "C": "f'(x) = e^(x²) * (ln(x) + 1/x)", "D": "f'(x) = 2x * e^(x²) * ln(x)"}),
            "correct_answer": "A",
            "explanation": "Sử dụng quy tắc tích: (uv)' = u'v + uv'. Với u = e^(x²), u' = 2x*e^(x²); v = ln(x), v' = 1/x. Vậy f'(x) = 2x*e^(x²)*ln(x) + e^(x²)*(1/x) = e^(x²)*(2x*ln(x) + 1/x)"
        },
        
        # Physics questions
        {
            "subject": "Vật lý",
            "topic": "Sóng cơ",
            "level": "easy",
            "content": "Sóng cơ là gì?",
            "options": json.dumps({"A": "Sự truyền dao động trong môi trường đàn hồi", "B": "Sự truyền ánh sáng trong chân không", "C": "Sự truyền điện tử trong kim loại", "D": "Sự truyền nhiệt trong chất rắn"}),
            "correct_answer": "A",
            "explanation": "Sóng cơ là sự truyền dao động của các hạt vật chất trong môi trường đàn hồi mà không có sự truyền chuyển dịch của vật chất"
        },
        {
            "subject": "Vật lý",
            "topic": "Sóng cơ",
            "level": "medium",
            "content": "Phương trình sóng đang truyền trên dây có dạng y = 0.02sin(10πt - 2πx). Tần số của sóng là bao nhiêu?",
            "options": json.dumps({"A": "5 Hz", "B": "10 Hz", "C": "2π Hz", "D": "10π Hz"}),
            "correct_answer": "A",
            "explanation": "Phương trình sóng tổng quát: y = A sin(ωt - kx). So sánh với y = 0.02sin(10πt - 2πx), ta có ω = 10π. Tần số f = ω/(2π) = 10π/(2π) = 5 Hz"
        },
        {
            "subject": "Vật lý",
            "topic": "Sóng cơ",
            "level": "hard",
            "content": "Một nguồn sóng có tần số 100 Hz phát sóng trong môi trường có tốc độ truyền 340 m/s. Bước sóng của sóng là bao nhiêu?",
            "options": json.dumps({"A": "3.4 m", "B": "34 m", "C": "0.34 m", "D": "340 m"}),
            "correct_answer": "A",
            "explanation": "Bước sóng λ = v/f = 340/100 = 3.4 m"
        },
        
        # Chemistry questions
        {
            "subject": "Hóa học",
            "topic": "Phản ứng oxi-hóa khử",
            "level": "easy",
            "content": "Phản ứng nào sau đây là phản ứng oxi-hóa khử?",
            "options": json.dumps({"A": "NaOH + HCl → NaCl + H₂O", "B": "Zn + H₂SO₄ → ZnSO₄ + H₂", "C": "CaCO₃ → CaO + CO₂", "D": "HCl + NH₃ → NH₄Cl"}),
            "correct_answer": "B",
            "explanation": "Trong phản ứng B, kẽm (Zn) bị oxi hóa từ 0 → +2, hydro (H) bị khử từ +1 → 0. Đây là phản ứng oxi-hóa khử"
        },
        {
            "subject": "Hóa học",
            "topic": "Phản ứng oxi-hóa khử",
            "level": "medium",
            "content": "Trong phản ứng: 2Fe + 3Cl₂ → 2FeCl₃. Chất oxi hóa là gì?",
            "options": json.dumps({"A": "Fe", "B": "Cl₂", "C": "FeCl₃", "D": "Cả Fe và Cl₂"}),
            "correct_answer": "B",
            "explanation": "Cl₂ có số oxi hóa giảm từ 0 → -1, nên Cl₂ là chất oxi hóa. Fe có số oxi hóa tăng từ 0 → +3, nên Fe là chất khử"
        },
        {
            "subject": "Hóa học",
            "topic": "Phản ứng oxi-hóa khử",
            "level": "hard",
            "content": "Cân bằng phản ứng oxi-hóa khử sau đây trong môi trường axit: MnO₄⁻ + Fe²⁺ → Mn²⁺ + Fe³⁺",
            "options": json.dumps({"A": "MnO₄⁻ + 5Fe²⁺ + 8H⁺ → Mn²⁺ + 5Fe³⁺ + 4H₂O", "B": "MnO₄⁻ + Fe²⁺ + 8H⁺ → Mn²⁺ + Fe³⁺ + 4H₂O", "C": "MnO₄⁻ + 5Fe²⁺ + 4H⁺ → Mn²⁺ + 5Fe³⁺ + 2H₂O", "D": "2MnO₄⁻ + 5Fe²⁺ + 16H⁺ → 2Mn²⁺ + 5Fe³⁺ + 8H₂O"}),
            "correct_answer": "A",
            "explanation": "Nửa phản ứng oxi hóa: Fe²⁺ → Fe³⁺ + e⁻ (nhân 5). Nửa phản ứng khử: MnO₄⁻ + 8H⁺ + 5e⁻ → Mn²⁺ + 4H₂O. Cộng lại ta được: MnO₄⁻ + 5Fe²⁺ + 8H⁺ → Mn²⁺ + 5Fe³⁺ + 4H₂O"
        },
        
        # English questions
        {
            "subject": "Tiếng Anh",
            "topic": "Câu bị động",
            "level": "easy",
            "content": "Chuyển câu sau sang bị động: 'They built this house last year.'",
            "options": json.dumps({"A": "This house was built last year.", "B": "This house is built last year.", "C": "This house built last year.", "D": "This house has been built last year."}),
            "correct_answer": "A",
            "explanation": "Câu bị động ở thì quá khứ đơn: S + was/were + V3 + (by O). 'They built' → 'was built'"
        },
        {
            "subject": "Tiếng Anh",
            "topic": "Câu bị động",
            "level": "medium",
            "content": "Chuyển câu sau sang bị động: 'Someone is painting the room now.'",
            "options": json.dumps({"A": "The room is being painted now.", "B": "The room is painted now.", "C": "The room being painted now.", "D": "The room has been painted now."}),
            "correct_answer": "A",
            "explanation": "Câu bị động ở thì hiện tại tiếp diễn: S + is/are + being + V3. 'is painting' → 'is being painted'"
        },
        {
            "subject": "Tiếng Anh",
            "topic": "Câu bị động",
            "level": "hard",
            "content": "Chuyển câu sau sang bị động: 'They will have completed the project by next month.'",
            "options": json.dumps({"A": "The project will have been completed by next month.", "B": "The project will be completed by next month.", "C": "The project will have completed by next month.", "D": "The project will have being completed by next month."}),
            "correct_answer": "A",
            "explanation": "Câu bị động ở thì tương lai hoàn thành: S + will + have + been + V3. 'will have completed' → 'will have been completed'"
        }
    ]
    
    try:
        # Check if questions already exist
        existing_count = db.query(Question).count()
        if existing_count > 0:
            print(f"ℹ️  Database already has {existing_count} questions. Skipping seeding.")
            return
        
        # Add sample questions
        for q_data in sample_questions:
            question = Question(**q_data)
            db.add(question)
        
        db.commit()
        print(f"✅ Successfully seeded {len(sample_questions)} questions into the database")
        
        # Verify seeding
        total_questions = db.query(Question).count()
        print(f"📊 Total questions in database: {total_questions}")
        
        # Show distribution
        subjects = db.query(Question.subject).distinct().all()
        for subject in subjects:
            count = db.query(Question).filter(Question.subject == subject[0]).count()
            print(f"   - {subject[0]}: {count} questions")
            
    except Exception as e:
        print(f"❌ Error seeding questions: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_questions()
