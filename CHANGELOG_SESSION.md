# Báo Cáo Tổng Hợp Xây Dựng QLSV-DJANGO (Fullstack Session)

> Tài liệu này tóm tắt toàn bộ tiến độ, kiến trúc và các module Frontend/Backend đã được xây dựng và hoàn thiện trong quá trình phát triển hệ thống Quản lý Sinh viên (QLSV-DJANGO).

---

## 1. TỔNG QUAN KIẾN TRÚC

Hệ thống được thiết kế theo mô hình **Client - Server (SPA)**:
* **Backend**: Django REST Framework (DRF), quản lý Database (PostgreSQL/Neon.tech), Auth JWT, cung cấp RESTful APIs.
* **Frontend**: React.js (Vite), dùng Tailwind CSS & shadcn/ui cho giao diện. Quản lý state bằng Zustand (Auth) và TanStack React Query (Server-state/Caching).

---

## 2. NHỮNG THAY ĐỔI VỀ BACKEND (DRF)

Để đáp ứng giao diện đa tính năng của Frontend, Backend đã được mở rộng thêm các Custom Endpoint và Serializer đặc thù để tối ưu hiệu suất (thay vì chỉ dùng CRUD mặc định).

### 2.1. API Quản lý Ghi danh (Enrollment)
* Thêm `ClassroomStudentSerializer` để map trực tiếp thông tin SV (tên, mssv, email) thông qua bảng trung gian.
* Tạo `ClassroomStudentViewSet` hỗ trợ filter sinh viên theo `classroom_id`.
* Route: `GET /POST /DELETE /api/academics/enrollments/`

### 2.2. API Dashboard & Thống kê
* Thêm class `DashboardView` tổng hợp toàn bộ số liệu: Tổng số SV/GV, Môn học, Tỉ lệ điểm danh 7 ngày qua, Top lớp đông sinh viên.
* Route: `GET /api/academics/dashboard/`

### 2.3. API Nhập Điểm & Kết Quả Học Tập (Exam Results)
* `GET /api/academics/exam-results/grade-sheet/`: Trả về danh sách sinh viên trong lớp kèm theo điểm cũ (nếu có) tạo thành bảng điểm trống để GV nhập.
* `POST /api/academics/exam-results/bulk-update/`: Cho phép lưu hàng loạt bảng điểm của cả lớp chỉ trong 1 request.
* `GET /api/academics/exam-results/student-gpa/`: Tính toán Tín chỉ tích lũy, GPA hệ 10 và GPA hệ 4 bằng Python (Backend).

---

## 3. NHỮNG THAY ĐỔI VỀ FRONTEND (REACT)

Frontend ban đầu chỉ có màn hình Login và 2 danh sách đơn giản. Hiện tại đã hoàn thiện thành một **Portal Quản lý Đào tạo** đầy đủ với **10 modules lớn**.

### 3.1. Các Module Quản lý Dữ liệu (CRUD)
Sử dụng Dialog forms kết hợp `useMutation` để làm Thêm/Sửa/Xóa mượt mà:
* **Học phần (Courses)**: Quản lý môn, số tín chỉ.
* **Lớp sinh hoạt (Classrooms)**: Quản lý lớp, khóa, học kỳ, GV chủ nhiệm.
* **Phân công giảng dạy (Assignments)**: Quản lý GV nào dạy môn nào, lớp nào (có validate chống trùng lặp).

### 3.2. Cấu Hình Hệ Thống (Academics Config)
* Xây dựng **Trang cấu hình gộp 3 Tabs**: Học kỳ, Khóa học, Loại kỳ thi.
* Giao diện gọn gàng, giúp Admin thiết lập dữ liệu nền mà không cần vào trang `/admin` gốc của Django.

### 3.3. Các Tính Năng Nghiệp Vụ (Bulk Operations)
* **SV trong Lớp (Enrollments)**: Giao diện Split-pane (trái chọn lớp, phải hiện SV). Có tính năng tìm kiếm và thêm SV vào lớp. Áp dụng **Optimistic Updates** giúp thao tác Thêm/Xóa SV diễn ra với độ trễ 0ms.
* **Điểm danh (Attendance)**: Nhập điểm danh theo Lớp + Ngày. Tích hợp radio buttons (Có mặt/Muộn/Vắng/Phép).
* **Nhập điểm (Enter Grades)**: Giao diện dạng Spreadsheet (bảng tính). Chọn filter (Học kỳ, Lớp, Môn, Loại kỳ thi) để bung ra bảng nhập điểm cho toàn lớp.

### 3.4. Cổng Thông Tin Sinh Viên (Student Portal)
* **Kết quả học tập**: Hiển thị 3 chỉ số lớn (Tín chỉ, GPA 10, GPA 4) thông qua Card UI, và bảng chi tiết điểm tổng kết từng môn học.

### 3.5. Dashboard & Sidebar Phân Quyền
* **Dashboard mới**: Hiển thị Biểu đồ cột điểm danh 7 ngày, Donut chart phân bố điểm danh, và Top lớp.
* **Sidebar Layout**: Render linh hoạt tùy vào `user.role` (Admin thấy toàn bộ, Giảng viên thấy lớp/nhập điểm, Sinh viên chỉ thấy GPA).

---

## 4. TỐI ƯU HÓA & FIX BUG (HIGHLIGHTS)

1. **Hiệu suất & Caching**: Sử dụng triệt để cơ chế invalidation của `React Query`. Ví dụ: Vừa thêm Môn học → tự động load lại API list.
2. **Optimistic Updates (Giao diện tức thì)**: Sửa vấn đề mạng chậm ở trang *Sinh viên trong lớp* bằng cách lừa UI cập nhật trước, gọi API ngầm sau.
3. **Sửa lỗi cấu trúc Dữ liệu**: Khắc phục lỗi nhầm lẫn giữa truyền Object vs ID khi POST payload lên Django.
4. **Vượt rào Cản UI**: Tự code CSS flex/grid các biểu đồ cột (Bar chart, Progress bar) trên Dashboard mà không cần cài thêm thư viện Recharts hay Chart.js nhằm giữ project nhẹ.

---

## 5. HƯỚNG DẪN DÀNH CHO NGƯỜI VÀO SAU

### Khởi chạy dự án
```bash
# Terminal 1: Backend
cd backend
venv\Scripts\activate
python manage.py runserver

# Terminal 2: Frontend
cd frontend
npm run dev
```

### Cách tiếp cận Codebase
* **Backend API**: Mọi logic phức tạp được viết ở `backend/academics/views.py` (sử dụng `@action(detail=False)`).
* **Frontend Hooks**: Các lệnh gọi API được gom hết vào `frontend/src/features/academics/hooks.js`. Nếu cần gọi API mới, hãy định nghĩa hàm ở file `api.js` sau đó bọc nó qua 1 custom hook `useQuery/useMutation` tại file này.

> **Trạng thái Database (Neon.tech)**: Vì dùng gói Free Tier, nếu thấy Backend quăng lỗi `psycopg2.OperationalError` không thể resolve DNS, nguyên nhân là DB đã bị Pause do không ai dùng trong 5 phút. Giải pháp: Vào console.neon.tech để ấn nút Resume.
