# 🚀 Hướng dẫn triển khai EduNexia lên Render.com

## 📋 Yêu cầu chuẩn bị

### 1. Tài khoản cần thiết
- **GitHub Account**: Để push code
- **Render Account**: Đăng ký tại [render.com](https://render.com)
- **Google Cloud Console**: Lấy Google OAuth credentials

### 2. Google OAuth Setup
1. Vào [Google Cloud Console](https://console.cloud.google.com/)
2. Tạo project mới
3. Enable **Google+ API** và **Google OAuth2 API**
4. Tạo OAuth 2.0 Client ID:
   - Application type: Web application
   - Authorized redirect URIs: `https://edunexia-api.onrender.com/api/v1/auth/google/callback`
5. Lưu **Client ID** và **Client Secret**

## 🛠️ Chuẩn bị Repository

### 1. Cấu trúc thư mục
```
edunexia/
├── app/                    # Backend FastAPI
├── frontend/               # Frontend React (nếu tách riêng)
├── public/                 # Static files
├── src/                   # React source
├── Dockerfile              # Backend Docker
├── render.yaml            # Render config
├── requirements.txt        # Python dependencies
├── package.json          # Node.js dependencies
└── alembic/             # Database migrations
```

### 2. Push code lên GitHub
```bash
git init
git add .
git commit -m "Ready for Render deployment"
git branch -M main
git remote add origin https://github.com/yourusername/edunexia.git
git push -u origin main
```

## 🚀 Triển khai trên Render

### Cách 1: Dùng render.yaml (Recommended)

1. **Vào Render Dashboard**
   - Click "New +" → "Web Service"
   - Connect GitHub repository
   - Chọn repository `edunexia`

2. **Cấu hình với render.yaml**
   - Render sẽ tự động đọc file `render.yaml`
   - Tự động tạo 3 services:
     - `edunexia-db` (PostgreSQL)
     - `edunexia-api` (FastAPI backend)
     - `edunexia-frontend` (React frontend)

3. **Cấu hình Environment Variables**
   Trong Render Dashboard, thêm các biến:
   ```
   GOOGLE_CLIENT_ID=your_google_client_id
   GOOGLE_CLIENT_SECRET=your_google_client_secret
   ```

### Cách 2: Manual Setup

#### 1. Database (PostgreSQL)
- "New +" → "PostgreSQL"
- Name: `edunexia-db`
- Plan: Free
- Region: Oregon (hoặc gần nhất)

#### 2. Backend (FastAPI)
- "New +" → "Web Service"
- Connect repository `edunexia`
- Name: `edunexia-api`
- Environment: Python 3
- Build Command: `pip install -r requirements.txt && python -m alembic upgrade head`
- Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Environment Variables:
  ```
  DATABASE_URL=[từ database connection string]
  SECRET_KEY=[auto-generate]
  ALGORITHM=HS256
  ENVIRONMENT=production
  FRONTEND_URL=https://edunexia-frontend.onrender.com
  GOOGLE_CLIENT_ID=[từ Google Console]
  GOOGLE_CLIENT_SECRET=[từ Google Console]
  ```

#### 3. Frontend (React)
- "New +" → "Static Site"
- Connect repository `edunexia`
- Name: `edunexia-frontend`
- Build Command: `npm install && npm run build`
- Publish Directory: `dist`
- Environment Variables:
  ```
  VITE_API_URL=https://edunexia-api.onrender.com
  VITE_GOOGLE_CLIENT_ID=[từ Google Console]
  ```

## 🔧 Cấu hình Production

### 1. CORS Configuration
Backend đã được cấu hình CORS trong `app/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 2. Database Migrations
Render sẽ tự động chạy:
```bash
python -m alembic upgrade head
```

### 3. Health Checks
- Backend: `/health` endpoint
- Database: Auto health check

## 🌐 URLs sau khi deploy

- **Frontend**: `https://edunexia-frontend.onrender.com`
- **Backend API**: `https://edunexia-api.onrender.com`
- **API Docs**: `https://edunexia-api.onrender.com/docs`

## ✅ Testing sau khi deploy

### 1. Kiểm tra API
```bash
curl https://edunexia-api.onrender.com/health
```

### 2. Test Authentication
- Truy cập frontend URL
- Đăng ký/đăng nhập user mới
- Test Google OAuth

### 3. Test Flow hoàn chỉnh
1. Tạo test
2. Làm bài
3. Nộp bài
4. Xem kết quả

## 🐛 Common Issues & Solutions

### 1. Database Connection Error
- Kiểm tra `DATABASE_URL` trong environment variables
- Đảm bảo database đã được tạo

### 2. CORS Error
- Kiểm tra `FRONTEND_URL` trong backend environment
- Đảm bảo URL chính xác

### 3. Google OAuth Error
- Kiểm tra redirect URI trong Google Console
- Đảm bảo `GOOGLE_CLIENT_ID` và `GOOGLE_CLIENT_SECRET` đúng

### 4. Build Failed
- Kiểm tra `requirements.txt` và `package.json`
- Xem build logs trong Render Dashboard

## 📊 Monitoring

### 1. Render Dashboard
- Logs: Xem real-time logs
- Metrics: CPU, Memory, Network
- Events: Deployment history

### 2. Database
- Connection pooling
- Backup settings (nếu dùng paid plan)

## 🔄 CI/CD Pipeline

Render tự động:
- Re-deploy khi push code mới
- Run database migrations
- Health checks

## 💡 Tips & Best Practices

1. **Environment Variables**: Luôn dùng production values
2. **Security**: Không commit sensitive data
3. **Database**: Sử dụng connection pooling
4. **Logging**: Enable detailed logs cho debugging
5. **Performance**: Optimize assets và database queries

## 🆘 Hỗ trợ

- **Render Docs**: [docs.render.com](https://docs.render.com)
- **Google OAuth**: [developers.google.com](https://developers.google.com)
- **FastAPI**: [fastapi.tiangolo.com](https://fastapi.tiangolo.com)

---

🎉 **Chúc mừng! EduNexia Learning Platform đã sẵn sàng hoạt động trên production!**
