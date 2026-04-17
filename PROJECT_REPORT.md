# Báo Cáo Dự Án: Hiện Đại Hóa Hệ Thống QLSV (University Edition)

Tài liệu này cung cấp cái nhìn tổng quan về kiến trúc, công nghệ và tiến độ hiện tại của dự án dành cho thành viên mới tham gia.

---

## 1. Tổng Quan & Mục Tiêu
Dự án được chuyển đổi từ nền tảng Django Template (Monolithic) sang kiến trúc hiện đại **Decoupled API-First**:
- **Backend:** Django REST Framework (DRF) đóng vai trò là API Server.
- **Frontend:** React (Vite) đóng vai trò là Single Page Application (SPA).
- **Đối tượng:** Hệ thống được thiết kế riêng cho quản lý sinh viên cấp **Đại học**.

---

## 2. Tech Stack (Công Nghệ Sử Dụng)

### Backend (Python/Django)
- **Framework:** Django 6.x + Django REST Framework.
- **Authentication:** JWT (SimpleJWT) - Đăng nhập nhận token.
- **Database:** PostgreSQL (Cloud - Neon.tech).
- **Excel Processing:** `openpyxl`.
- **Testing:** `pytest` + `pytest-django` + `model-bakery`.

### Frontend (JavaScript/React)
- **Build Tool:** Vite.
- **Styling:** Tailwind CSS + **shadcn/ui** (Bộ component hiện đại).
- **State Management:** Zustand (Auth/Settings).
- **Data Fetching:** TanStack Query v5 (React Query).
- **Icons:** Lucide React.

---

## 3. Cấu Trúc Thư Mục (Directory Structure)

### `/backend`
- `accounts/`: Quản lý User, vai trò (Admin, Giảng viên, Sinh viên) và Auth.
- `students/`: Quản lý hồ sơ sinh viên, liên hệ khẩn cấp và tính năng Excel.
- `teachers/`: Quản lý thông tin Giảng viên và Khoa/Bộ môn.
- `academics/`: Chứa core logic về Khóa (Grade), Lớp sinh hoạt (Classroom), Học phần (Course) và Điểm số.

### `/frontend`
- `src/api/`: Cấu hình `axiosClient` và các service API chung.
- `src/features/`: Chia theo module (students, teachers, academics). Mỗi module có `api.js` và `hooks.js` (React Query).
- `src/components/ui/`: Các component nguyên tử từ shadcn.
- `src/pages/`: Các màn hình chính của ứng dụng.

---

## 4. Tiến Độ Hiện Tại (Kết Thúc Phase 2)

### ✅ Đã hoàn thành (100%):
1. **Refactor Đại học:** Chuyển đổi toàn bộ thuật ngữ (Giảng viên, Khóa, Lớp sinh hoạt).
2. **Hệ thống Sinh viên:** CRUD đầy đủ + **Import/Export Excel**.
3. **Hệ thống Giảng viên:** CRUD đầy đủ.
4. **Academics Foundation:** Đã có giao diện danh sách cho Khóa, Học phần, Lớp sinh hoạt.
5. **Testing:** Đã có bộ test backend và frontend ổn định.

### 🚧 Đang thực hiện (Phase 3):
1. Hoàn thiện Form Thêm/Sửa cho Lớp sinh hoạt & Học phần.
2. Xây dựng logic **Phân công giảng dạy** (Course Assignments).
3. Hệ thống **Điểm danh (Attendance)**.

---

## 5. Hướng Dẫn Cài Đặt (Cho Người Mới)

### Bước 1: Clone Repo & Backend Setup
```bash
git clone https://github.com/tungm1204-sudo/QLSV-DJANGO
cd QLSV-DJANGO/backend
# Tạo venv và cài dependencies (nếu có requirements.txt)
python manage.py migrate
python manage.py runserver
```

### Bước 2: Frontend Setup
```bash
cd ../frontend
npm install
npm run dev
```

### Bước 3: Tài khoản Test
- **Trang Login:** `http://localhost:5173/login`
- **Tài khoản Admin:** `admin` / `password123`

---

## 6. Lưu Ý Quan Trọng Cho Dev Mới
- **University Logic:** Luôn sử dụng thuật ngữ "Lớp sinh hoạt" thay vì "Lớp học" để tránh nhầm lẫn với "Lớp học phần".
- **API First:** Mọi thao tác frontend phải thông qua `axiosClient` trong `src/api/`.
- **UI Consistency:** Sử dụng bộ component trong `src/components/ui/`.

---
> *Tài liệu cập nhật ngày: 18/04/2026 bởi Antigravity AI.*
