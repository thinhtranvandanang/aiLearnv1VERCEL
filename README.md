
# EduNexia Learning Platform 🚀

Nền tảng học tập thông minh tích hợp AI dành cho học sinh thế hệ mới.

## 🌟 Tính năng cốt lõi
- **AI Practice**: Tự động tạo đề thi theo yêu cầu (Môn học, Chủ đề, Độ khó).
- **OCR Grader**: Chấm điểm bài làm qua ảnh chụp (Nộp bài Offline).
- **Smart Analytics**: Phân tích lỗ hổng kiến thức và gợi ý lộ trình học tập.
- **Hybrid Auth**: Đăng nhập đa phương thức (Username/Password & Google OAuth).

## 🛠️ Công nghệ sử dụng
- **Frontend**: React 19, Tailwind CSS, React Router 6, Axios.
- **Backend**: FastAPI, SQLAlchemy 2.0, PostgreSQL.
- **Auth**: JWT, Google OAuth 2.0.

## 🚀 Cài đặt nhanh
### 1. Backend
```bash
pip install -r requirements.txt
python -m app.main
```
*Lưu ý: Cấu hình `.env` với Google Client ID để sử dụng tính năng Google Login.*

### 2. Frontend
- Mở `index.html` qua **Live Server** trong Cursor/VSCode.
- Hoặc dùng `npx vite`.

## 📌 Luồng xác thực Google
1. Người dùng nhấn "Đăng nhập bằng Google".
2. Frontend chuyển hướng tới: `http://localhost:8000/api/v1/auth/google/login`.
3. Google xác thực -> Trả code về Backend.
4. Backend đổi code lấy Token -> Chuyển hướng về Frontend kèm JWT: `http://localhost:3000/login?token=...`.
5. Frontend lưu Token và vào Dashboard.
