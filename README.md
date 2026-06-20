# QLSV-DJANGO: Hệ Thống Quản Lý Sinh Viên

> Dự án hiện đại hóa quản lý sinh viên cấp Đại học, áp dụng kiến trúc **Decoupled API-First** (Django REST Framework + React Vite).

---

## 1. Công Nghệ Sử Dụng (Tech Stack)
- **Backend:** Django 6.x, DRF, JWT Auth (HttpOnly Cookies), PostgreSQL (Neon Cloud), pytest.
- **Frontend:** React 19 (Vite), Tailwind CSS v4, shadcn/ui, TanStack Query v5, Zustand.
- **DevOps:** GitHub Actions (CI/CD tự động chạy Lint & Pytest).

---

## 2. Cấu Trúc & Luồng Dữ Liệu
### Kiến trúc Client-Server
1. **Frontend (`/frontend`)**: Đóng vai trò là một SPA. Gọi API qua `axiosClient`. Trạng thái xác thực lưu tại Zustand, dữ liệu API cache bởi TanStack Query. Code logic nghiệp vụ tập trung ở `src/features/`.
2. **Backend (`/backend`)**: API Server. Phân quyền chặt chẽ bằng Custom Permissions. Các module chính: `accounts/`, `students/`, `teachers/`, `academics/`.

### Nghiệp Vụ Người Dùng
- **Admin / Giáo vụ:** Quản lý toàn diện (Khóa, Học kỳ, Lớp sinh hoạt, Môn học, Phân công giảng dạy).
- **Giảng viên:** Theo dõi lớp, Điểm danh hàng loạt (Bulk Update), Nhập bảng điểm.
- **Sinh viên:** Tra cứu thông tin cá nhân, điểm số, điểm trung bình (GPA).

---

## 3. Nhật Ký Phát Triển (Tính năng nổi bật)
- **Quản lý dữ liệu:** CRUD mượt mà cho Sinh viên, Giảng viên. Hỗ trợ Import/Export bằng Excel.
- **Trải nghiệm người dùng (UX):** Áp dụng *Optimistic Updates* (cập nhật UI tức thì trước khi gọi API) ở các chức năng thêm/xóa sinh viên. Các danh sách hỗ trợ Filter nhanh gọn.
- **Bảo mật & Hiệu năng:**
  - Token Refresh được bảo mật tuyệt đối qua **HttpOnly Cookies** (Ngăn chặn XSS).
  - Tối ưu truy vấn ORM bằng `select_related`/`prefetch_related` nhằm dọn dẹp lỗi N+1 Query.
  - Role-based Access Control (RBAC): Chặn quyền tùy thuộc theo role (Admin, Teacher, Student).

---

## 4. Hướng Dẫn Cài Đặt (Local Setup)

```bash
# 1. Khởi chạy Backend
cd backend
venv\Scripts\activate # Kích hoạt môi trường ảo (nếu có)
python manage.py runserver

# 2. Khởi chạy Frontend
cd frontend
npm install
npm run dev
```

**Tài khoản Test:** `admin` / `password123`
**URL Đăng nhập:** `http://localhost:5173/login`

> **Lưu ý Database (Neon.tech):** Nếu hệ thống báo lỗi `psycopg2.OperationalError`, nguyên nhân là do DB gói Free Tier tự động bị ngủ đông (Pause) sau 5 phút. Giải pháp: Đăng nhập vào console.neon.tech để ấn "Resume".
