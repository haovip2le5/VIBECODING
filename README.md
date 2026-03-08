# Student Management System

## 👤 Thông tin cá nhân
- **Tên**: Trần Nhựt Hào
- **MSSV**: 23674431
- **Lớp**: DHKHDL19A

## 🛠️ Tech Stack
- **Backend**: FastAPI (Python)
- **Frontend**: React JS (JavaScript)
- **Database**: SQLite
- **API Communication**: Axios
- **ORM**: SQLAlchemy

## 🎯 Tools & Platform
- **Code Editors**: Lovable, Cursor, Windsurf
- **Development Tools**: Angrivity
- **Version Control**: Git
- **Database**: SQLite
- **Package Managers**: pip (Python), npm (Node.js)
- **Runtime**: Python 3.12, Node.js

## 📋 Log - Quá trình thực hiện

### **Phiên bản 1.0 - MVP (Minimum Viable Product)**
- ✅ Xây dựng cấu trúc dự án: Backend (FastAPI) + Frontend (React)
- ✅ Backend: Tạo các endpoint CRUD cơ bản cho sinh viên
  - `GET /students` - Lấy danh sách sinh viên
  - `POST /students` - Thêm sinh viên mới
  - `PUT /students/{id}` - Cập nhật sinh viên
  - `DELETE /students/{id}` - Xóa sinh viên
- ✅ Database: Cài đặt SQLite với SQLAlchemy ORM
- ✅ Frontend: Giao diện bảng danh sách sinh viên và form thêm/sửa
- ✅ CORS: Cấu hình cho phép frontend kết nối backend
- ✅ Backend chạy trên port 8000, Frontend trên port 3000

### **Phiên bản 2.0 - Extended Features**
- ✅ **Yêu cầu 1**: Thêm lớp học
  - Tạo bảng `Class` với: class_id, class_name, advisor
  - Endpoint: `GET /classes`, `POST /classes`
  
- ✅ **Yêu cầu 2**: Sinh viên thuộc lớp
  - Thêm trường `class_id` vào bảng Student (Foreign Key)
  - Hiển thị tên lớp trong danh sách sinh viên
  
- ✅ **Yêu cầu 3**: Tìm kiếm sinh viên
  - Endpoint: `GET /students?name=<search_term>`
  - UI: Search box để tìm theo tên
  
- ✅ **Yêu cầu 4**: Thống kê
  - Endpoint: `GET /statistics`
  - Hiển thị: Tổng số sinh viên, GPA trung bình, số sinh viên theo ngành
  
- ✅ **Yêu cầu 5**: Xuất dữ liệu
  - Endpoint: `GET /export/csv`
  - Chức năng: Export dữ liệu sinh viên ra file CSV
  - Nút "Export to CSV" trên giao diện

### **Phiên bản 2.1 - Seed Data**
- ✅ Tạo file `seed_data.py` để tự động generate dữ liệu mẫu
- ✅ Tạo file `data_sample.csv` với dữ liệu mẫu
- ✅ Dữ liệu mẫu: 3 lớp học + 8 sinh viên

## 📦 Cấu trúc dự án
```
vibecode2/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── requirements.txt         # Python dependencies
│   ├── seed_data.py            # Script generate dữ liệu
│   ├── data_sample.csv         # File dữ liệu mẫu
│   └── students.db             # SQLite database
├── frontend/
│   ├── src/
│   │   ├── App.js              # Main React component
│   │   ├── App.css             # Stylesheet
│   │   ├── index.js            # Entry point
│   │   └── index.css           # Global styles
│   ├── public/
│   │   └── index.html
│   └── package.json
└── README.md

## 🚀 Cách chạy ứng dụng

### Backend:
```bash
cd backend
pip install -r requirements.txt
python main.py
```
Backend sẽ chạy trên: `http://localhost:8000`
API Docs (Swagger): `http://localhost:8000/docs`

### Frontend:
```bash
cd frontend
npm install
npm start
```
Frontend sẽ chạy trên: `http://localhost:3000`

### Seed dữ liệu (Tuỳ chọn):
```bash
cd backend
python seed_data.py
```

## 📊 Các chức năng chính
1. **Quản lý sinh viên**: Thêm, sửa, xóa, xem danh sách
2. **Quản lý lớp học**: Thêm, sửa, xóa lớp (qua Swagger)
3. **Tìm kiếm**: Tìm sinh viên theo tên
4. **Thống kê**: Xem tổng SV, GPA trung bình, SV theo ngành
5. **Xuất dữ liệu**: Export dữ liệu sang file CSV

## 📝 Ghi chú
- Backend phải chạy TRƯỚC khi mở web
- Database tự động tạo bảng khi chạy lần đầu
- CORS được cấu hình cho `http://localhost:3000`

### Phần 1 (CRUD cơ bản)
- Thêm sinh viên
- Xem danh sách sinh viên
- Sửa thông tin sinh viên
- Xóa sinh viên

### Phần 2 (Mở rộng)
- Quản lý lớp học
- Tìm kiếm sinh viên theo tên
- Xem thống kê (tổng, GPA, by major)
- Xuất dữ liệu CSV