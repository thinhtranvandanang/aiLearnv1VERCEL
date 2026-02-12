
# EduNexia API Documentation v1.2

## 🔑 Authentication
Tất cả các API (trừ Auth công khai) đều yêu cầu Header:
`Authorization: Bearer <JWT_TOKEN>`

### Auth Endpoints
- `POST /auth/student/login`: Đăng nhập truyền thống.
- `POST /auth/student/register`: Đăng ký tài khoản.
- `GET /auth/google/login`: Khởi tạo luồng Google OAuth.
- `GET /auth/google/callback`: Backend xử lý code từ Google.

## 📝 Practice Tests
- `POST /practice-tests/generate`: Tạo đề thi AI.
- `GET /practice-tests/{id}/content`: Lấy nội dung câu hỏi.
- `POST /practice-tests/{id}/submit-online`: Nộp bài trực tiếp.
- `POST /practice-tests/{id}/submit-offline`: Nộp bài qua ảnh chụp (Multipart).

## 📊 Analytics & History
- `GET /submissions/{id}/result`: Xem kết quả chi tiết.
- `GET /submissions/{id}/learning-suggestions`: Gợi ý kiến thức từ AI.
- `GET /students/me/learning-history`: Lịch sử học tập tổng quát.
