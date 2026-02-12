# Hướng Dẫn Triển Khai EduNexia Lên Vercel

Hướng dẫn này sẽ giúp bạn triển khai ứng dụng EduNexia (Frontend React + Backend FastAPI) lên nền tảng đám mây Vercel.

## Tổng Quan Kiến Trúc Triển Khai

Việc triển khai lên Vercel bao gồm 3 phần chính được deploy **cùng lúc trên một domain**:

1.  **Frontend (React)**: 
    - Được Vercel build tự động thành Static Site
    - Vercel đảm nhận việc routing cho Single Page Application (SPA)
    - Truy cập qua URL gốc: `https://your-app.vercel.app`

2.  **Backend (FastAPI)**: 
    - **Tự động** được chuyển đổi thành **Serverless Functions**
    - Vercel phát hiện code Python trong thư mục `api/` và tự động package
    - Không cần cấu hình server riêng - Vercel xử lý tất cả
    - API endpoints truy cập qua: `https://your-app.vercel.app/api/*`
    - **Lưu ý**: Backend không chạy liên tục như VPS, mà chỉ khởi động khi có request (serverless)

3.  **Cơ Sở Dữ Liệu (PostgreSQL)**: 
    - Vercel không lưu trữ database trực tiếp
    - Bạn cần sử dụng dịch vụ database bên ngoài (Vercel Postgres, Supabase, Neon, v.v.)
    - Kết nối qua biến môi trường `DATABASE_URL`

## Các File Cấu Hình Quan Trọng

- `vercel.json`: Điều hướng request. Request bắt đầu bằng `/api/` sẽ vào Serverless Function, các request khác sẽ vào Frontend.
- `api/index.py`: Điểm nhập (entry point) cho Vercel biết cách khởi chạy Backend.
- `requirements.txt`: Danh sách thư viện Python cần thiết cho Serverless Function.

## Quy Trình Triển Khai Chi Tiết

### Bước 1: Chuẩn Bị Code (Đã Thực Hiện)
Chúng ta đã tạo các file cần thiết:
- `vercel.json` đã được cấu hình rewrite.
- `api/index.py` đã được tạo để expose `app`.

### Bước 2: Đẩy Code Lên GitHub
Đảm bảo code mới nhất của bạn đã được push lên repository GitHub của bạn.

### Bước 3: Tạo Project Trên Vercel
1.  Truy cập [Vercel Dashboard](https://vercel.com/dashboard) và đăng nhập.
2.  Nhấn **"Add New..."** -> **"Project"**.
3.  Chọn repository **EduNexia** từ GitHub của bạn và nhấn **Import**.

### Bước 4: Tạo Cơ Sở Dữ Liệu (Quan trọng)
Vì bạn chưa có database, cách nhanh nhất là dùng **Vercel Postgres** ngay trong project:
1. Trong dashboard project trên Vercel, chọn tab **Storage**.
2. Chọn **Connect Database** -> **Create New** -> **Postgres**.
3. Đặt tên (ví dụ: `edunexia-db`) và chọn vùng (Region) gần bạn nhất (ví dụ: Singapore).
4. Sau khi tạo xong, nhấn **Connect**. Vercel sẽ tự động tạo một biến môi trường tên là **`POSTGRES_URL`** (hoặc `DATABASE_URL`) cho bạn. Bạn không cần phải copy manual nếu dùng cách này!

### Bước 5: Cấu Hình Biến Môi Trường (Environment Variables)
Trong tab **Settings** -> **Environment Variables**, hãy nhập các biến sau:

    | Tên Biến | Giá Trị Ví Dụ / Mô Tả |
    | :--- | :--- |
    | `DATABASE_URL` | Lấy từ tab Storage (thường là `${POSTGRES_URL}`) |
    | `SECRET_KEY` | Chuỗi bí mật (đã tạo ở bước trước) |
    | `ALGORITHM` | `HS256` |
    | `GEMINI_API_KEY` | API Key của Gemini AI |
    | `ENVIRONMENT` | `production` |
    | `BACKEND_CORS_ORIGINS` | `*` (Lần đầu cứ để dấu sao) |

> [!TIP]
> **Về `BACKEND_CORS_ORIGINS`**: Vì bạn chưa deploy nên chưa có URL chính thức. 
> 1. Lần đầu deploy: Bạn có thể để trống hoặc điền `*` để test.
> 2. Sau khi deploy xong: Vercel sẽ cấp cho bạn một URL (ví dụ: `https://ailearnv1vercel.vercel.app`). Lúc đó bạn quay lại phần **Settings -> Environment Variables** trên Vercel, cập nhật biến này thành URL đó và redeploy để bảo mật hơn.

### Cách tạo `SECRET_KEY` bảo mật
Bạn nên sử dụng một chuỗi ngẫu nhiên dài và phức tạp. Có 2 cách đơn giản để tạo:

**Cách 1: Dùng Python (Khuyên dùng)**
Chạy lệnh này trong terminal của bạn:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```
Nó sẽ in ra một chuỗi như `_u5Y8Xp9jR...`. Hãy copy chuỗi đó làm `SECRET_KEY`.

**Cách 2: Dùng OpenSSL (Nếu có cài đặt)**
```bash
openssl rand -hex 32
```

### Tại sao dùng `HS256`?
`HS256` (HMAC with SHA-256) là thuật toán tiêu chuẩn và phổ biến nhất cho JWT. Nó sử dụng một khóa bí mật duy nhất (`SECRET_KEY`) để cả ký và xác thực token. Đây là cấu hình mặc định trong code Backend của bạn.

> [!IMPORTANT]
> **Lưu ý về Database**: Bạn có thể tạo **Vercel Postgres** ngay trong tab **Storage** của project Vercel và nó sẽ tự động điền `DATABASE_URL` cho bạn.

### Bước 5: Deploy
Nhấn nút **Deploy**. Vercel sẽ tiến hành build frontend và cài đặt dependencies cho backend.
Quá trình này mất khoảng 2-5 phút.

### Bước 6: Kiểm Tra
Sau khi deploy thành công:
1.  Truy cập URL project (vd: `https://edunexia.vercel.app`).
2.  Kiểm tra trang chủ có load không.
3.  Kiểm tra gọi API (ví dụ: đăng nhập) xem có hoạt động không.

---

## Xử Lý Sự Cố Thường Gặp

**Lỗi 404 trên các trang con khi reload**:
- Nguyên nhân: Routing SPA chưa đúng.
- Giải pháp: Kiểm tra `vercel.json`, đảm bảo có rewrite `source: "/(.*)"` về `/index.html`.

**Lỗi 500 khi gọi API**:
- Nguyên nhân: Lỗi code Backend hoặc kết nối Database.
- Giải pháp: Vào tab **Logs** trên Vercel, chọn Filter là **Functions** để xem chi tiết lỗi Python.

**Lỗi "Module not found" ở Backend**:
- Nguyên nhân: Thiếu thư viện trong `requirements.txt`.
- Giải pháp: Bổ sung tên thư viện vào file và push lại code.
