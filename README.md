# Student Management System

## Thông tin cá nhân
- Tên: [Tên của bạn]
- MSSV: [Mã sinh viên]
- Lớp: [Lớp]

## Tech Stack
- Backend: FastAPI (Python)
- Frontend: React (JavaScript)
- Database: SQLite

## Tools
- VS Code
- Python 3.12
- Node.js
- Git

## Log
### Phiên bản 1 (MVP)
- Tạo cấu trúc dự án với backend (FastAPI) và frontend (React)
- Backend: API CRUD cho sinh viên với SQLAlchemy và SQLite
- Frontend: Giao diện bảng danh sách và form thêm/sửa sinh viên
- Chạy backend trên port 8000, frontend trên port 3000
- CORS enabled để frontend kết nối backend

## Cách chạy
1. Backend:
   ```
   cd backend
   pip install -r requirements.txt
   python main.py
   ```
2. Frontend:
   ```
   cd frontend
   npm install
   npm start
   ```
3. Truy cập http://localhost:3000

## Chức năng
- Thêm sinh viên
- Xem danh sách sinh viên
- Sửa thông tin sinh viên
- Xóa sinh viên