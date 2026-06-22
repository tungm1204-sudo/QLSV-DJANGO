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

## 3. Nhật Ký Phát Triển (Changelog)

Theo dõi tiến trình xây dựng dự án qua từng giai đoạn (Phase). Khi có Phase mới, các cập nhật sẽ được thêm nối tiếp vào đây.

### Phase 1 & 2: Xây Dựng Nền Tảng & Các Module Cơ Bản
- **Authentication & Security:** Sử dụng JWT cho xác thực, phân quyền mạnh mẽ giữa Sinh viên, Giảng viên, và Admin.
- **Backend API:** Hệ thống RESTful API được xây dựng bằng Django REST Framework.
- **Seed Data:** Cung cấp script tự động tạo dữ liệu mẫu (`seed_data.py`) cho hệ thống.
- **Testing:** Đã được kiểm thử tự động toàn diện qua các vòng đời nghiệp vụ từ Auth, Academics đến Finance.

### Phase 3: Hoàn Thiện Nghiệp Vụ Frontend (UX/UI)
- **Ghi danh (Enrollment):** Áp dụng **Optimistic Updates** giúp thao tác thêm/xóa sinh viên khỏi lớp phản hồi ngay lập tức trên UI (độ trễ 0ms).
- **Điểm danh (Attendance):** Cấu hình tính năng Bulk Update (lưu hàng loạt) cho danh sách điểm danh theo lớp và ngày.
- **Phân công giảng dạy:** Tạo bảng danh sách phân công với tính năng Filter trực tiếp (chọn Lớp, Môn Học, Giảng Viên) gửi qua Query Params.
- **Nhập điểm:** Cấu hình form nhập điểm hiển thị dạng Spreadsheet tiện lợi.

### Phase 4: Nợ Kỹ Thuật (Nâng cấp Hệ Thống & Bảo Mật)
- **Hiệu suất Database (N+1 Query):** Rà soát toàn bộ DRF ViewSet, bổ sung `select_related`/`prefetch_related` giúp dọn dẹp triệt để tình trạng query lặp.
- **Bảo mật JWT Token:** Chuyển đổi phương thức lưu `refresh_token` từ `localStorage` sang **HttpOnly Cookies** để ngăn chặn tấn công XSS. Backend và Frontend đều được custom để gửi nhận cookie tự động.
- **Phân quyền Custom (DRF Permissions):** Cấu trúc lại bảo mật ở backend bằng các class quyền (vd: `IsAdminOrReadOnly`, `IsAdminOrTeacher`) chặn đứng các thao tác trái phép theo Role (Admin, Giáo vụ, Giảng viên, Sinh viên).
- **CI/CD Pipeline:** Triển khai GitHub Actions (`ci.yml`) để tự động kiểm thử code mỗi khi Push/Pull Request (chạy `pytest` cho Python và `eslint` cho React).

### Phase 5: Cổng Thông Tin Cá Nhân Hóa (Portals & Personalization)
- **Kiến trúc dữ liệu an toàn:** Ghi đè `get_queryset` theo `user.role` để lọc dữ liệu ở Backend. Giảng viên chỉ xem được lớp mình phụ trách, Sinh viên chỉ thấy dữ liệu của chính mình mà không cần tách các endpoint riêng biệt.
- **Giao diện Sinh Viên:** Ra mắt trang "Thời khóa biểu & Lịch sử điểm danh" độc lập, hiển thị trực quan các môn học đã đăng ký.
- **Giao diện Giảng Viên:** Ẩn hoàn toàn tính năng Thêm/Sửa/Xóa lớp học/phân công, bảo vệ an toàn dữ liệu khỏi các thao tác nhầm lẫn.

### Phase 5.5: Tái Cấu Trúc (Refactor) Ứng dụng Academics
- **Chia nhỏ `views.py` & `serializers.py`:** Phân rã mã nguồn nguyên khối thành các package nhỏ gọn (`core_views`, `classroom_views`, `attendance_views`, `exam_views`) giúp dễ bảo trì và khoanh vùng lỗi.
- **Giữ nguyên định tuyến (Transparent Integration):** Sử dụng `__init__.py` để expose các class ra ngoài nên `urls.py` không cần thay đổi.

### Phase 5.6: Tái Cấu Trúc (Refactor) Frontend Academics
- **Module Hóa API & Hooks:** Phân rã `academics.js` và `hooks.js` (hơn 300 dòng) thành các file theo từng tính năng tương ứng với Backend (Core, Classrooms, Attendance, Exams).
- **Barrel Export:** Giữ nguyên các đường dẫn import ở UI thông qua `index.js`, đảm bảo UI không đứt gãy.

### Phase 6: Quản Lý Tài Chính & Học Phí (Tuition & Fees)
- **Tự động hóa học phí:** Xây dựng module `finance` để tính toán học phí sinh viên cần đóng dựa trên tổng số tín chỉ đã đăng ký.
- **Trang Quản lý Học phí:** Phát triển giao diện cho phép Kế toán/Admin xem danh sách, lọc theo trạng thái (Nợ/Đã nộp) và xác nhận thu tiền.
- **Chi tiết môn học:** Tích hợp tính năng hiển thị chi tiết từng môn học (tên môn, số tín chỉ) đi kèm với mỗi khoản học phí để sinh viên tiện theo dõi.

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
