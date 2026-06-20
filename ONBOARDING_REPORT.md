# Báo Cáo Onboarding Dự Án Chi Tiết (A-Z)

Chào mừng bạn tham gia dự án! Dưới đây là báo cáo phân tích toàn diện về hệ thống hiện tại, giúp bạn nhanh chóng nắm bắt kiến trúc và tự tin đóng góp vào dự án.

---

## 1. Tổng Quan Dự Án & Nghiệp Vụ (Business Logic)

> [!NOTE]
> **Bài toán giải quyết:** Đây là hệ thống quản lý sinh viên dành riêng cho môi trường **Đại học**. Dự án đang trong quá trình chuyển đổi (hiện đại hóa) từ nền tảng web monolithic truyền thống (Django Template) sang kiến trúc Decoupled API-First hiện đại.

- **Đối tượng người dùng hướng đến:**
  - **Admin / Giáo vụ (Academic Staff):** Quản lý cấu hình toàn hệ thống, tạo dữ liệu gốc (Khoa, Khóa, Môn học, Lớp), cấu hình học kỳ và phân công giảng dạy.
  - **Giảng viên (Teacher):** Quản lý thông tin lớp sinh hoạt/lớp học phần được phân công, thực hiện điểm danh và nhập điểm sinh viên.
  - **Sinh viên (Student):** Tra cứu thông tin cá nhân, xem điểm số, thời khóa biểu và lịch sử điểm danh.

- **Tóm tắt các chức năng cốt lõi (Core Features):**
  - **Hệ thống Tài khoản & Phân quyền:** Quản lý người dùng tập trung với Role-based Access Control (Admin, Giáo vụ, Giảng viên, Sinh viên).
  - **Quản lý Hồ sơ (Profiles):** Quản lý chi tiết sinh viên (kèm liên hệ khẩn cấp/phụ huynh) và giảng viên (kèm thông tin khoa/bộ môn). Hỗ trợ Import/Export Excel dữ liệu sinh viên.
  - **Nghiệp vụ Học vụ (Academics):** Quản lý cấu trúc đào tạo bao gồm Học kỳ, Khóa, Lớp sinh hoạt, Môn học, Phân công giảng dạy, Điểm danh và Quản lý Điểm số. (Ví dụ API điểm danh: `bulk-update` và `attendance-sheet` đã hoàn thiện; API Phân công giảng dạy `/api/assignments/` đã hỗ trợ filter theo Lớp/Môn/GV và trả về tên chi tiết để làm UI).

---

## 2. Chi Tiết Bản Đồ Công Nghệ (Tech Stack Analysis)

Dự án sử dụng một stack công nghệ rất hiện đại, chia tách rõ ràng giữa Frontend và Backend.

| Tên Công Nghệ/Thư Viện | Vai trò/Tác dụng cụ thể | Đánh giá phiên bản |
| :--- | :--- | :--- |
| **Django (v5.0+)** | Framework cốt lõi ở Backend, quản lý ORM, Model, và logic nghiệp vụ. | Mới, bảo mật cao. |
| **Django REST Framework (DRF)** | Xây dựng hệ thống API (RESTful) giao tiếp với Frontend. API-First thay vì SSR. | Chuẩn công nghiệp, ổn định. |
| **SimpleJWT** | Xác thực người dùng (Authentication) qua JSON Web Token (Access/Refresh token). | Lựa chọn tốt nhất cho SPA. |
| **PostgreSQL (Neon Cloud)** | Database chính trên môi trường production, lưu trữ dữ liệu quan hệ. | Hiện đại, cloud-native. |
| **SQLite / pytest-django** | Database nhẹ dùng cho môi trường dev/testing để test chạy siêu tốc. | Phù hợp cho CI và Dev local. |
| **openpyxl** | Thư viện xử lý nghiệp vụ Import/Export danh sách sinh viên qua file Excel (`.xlsx`). | Tiêu chuẩn và ổn định. |
| **React (v19) + Vite (v8)** | Frontend Single Page Application (SPA). Vite giúp build và reload cực nhanh thay vì CRA/Webpack. | Rất mới, hiệu năng tối đa. |
| **Tailwind CSS (v4) + shadcn/ui** | Styling UI. Tailwind giúp style nhanh, `shadcn/ui` cung cấp các component đẹp, có thể tùy biến source code. | Đang cực kỳ trending. |
| **TanStack Query (v5)** | React Query quản lý server-state: tự động fetch, cache, và đồng bộ dữ liệu API. | Phiên bản mới, tối ưu tốt. |
| **Zustand (v5)** | Quản lý global client-state gọn nhẹ (như session user, auth token). | Nhẹ và dễ hiểu hơn Redux. |
| **React Hook Form + Zod** | Xử lý trạng thái Form và validate dữ liệu chặt chẽ dựa trên schema. | Combo tiêu chuẩn hiện nay. |

---

## 3. Kiến Trúc Hệ Thống & Luồng Dữ Liệu (Architecture & Data Flow)

> [!TIP]
> **Kiến trúc:** Hệ thống áp dụng mô hình **Decoupled Client-Server**. Backend thuần túy chỉ trả về JSON qua API, và Frontend là một SPA hoàn toàn độc lập.

### Thiết kế Database (Models)
Các model được chia rành mạch theo từng domain nghiệp vụ:
- Bảng **`User`** (AbstractUser) đóng vai trò trung tâm để đăng nhập, đi kèm trường `role`.
- Bảng **`StudentProfile`** và **`TeacherProfile`** liên kết `OneToOne` với `User` để mở rộng thông tin.
- Module Học vụ xoay quanh: **`Grade`** (Khóa) -> **`Classroom`** (Lớp sinh hoạt) -> chứa **`ClassroomStudent`** (M-N).
- Lớp học gắn với **`Semester`** (Học kỳ) và có phân công **`CourseAssignment`** cho Giảng viên dạy Môn học (**`Course`**).

### Luồng Dữ Liệu (Data Flow) - Ví dụ luồng Đăng nhập:
1. **User Action:** Người dùng điền Form Login ở Frontend. `React Hook Form` kết hợp `Zod` validate email/password ngay tại client.
2. **API Call:** Hàm xử lý gọi API login thông qua `axiosClient` (`POST /api/token/`).
3. **Backend Auth:** DRF nhận request, xác thực qua model `User`. Nếu đúng, `SimpleJWT` sinh ra `access_token` và `refresh_token` trả về JSON.
4. **Client State:** Frontend nhận token, lưu vào `Zustand` store (hoặc localStorage) để duy trì phiên.
5. **Next Request:** Khi Frontend muốn lấy danh sách sinh viên, `TanStack Query` gọi API kèm Header `Authorization: Bearer <token>`. DRF nhận token, phân quyền (Permissions), query Model qua ORM, Serializer chuyển đổi thành JSON và trả về cho React render bảng.

---

## 4. Cấu Trúc Thư Mục & Cách Tiếp Cận Code (Codebase Navigation)

### Backend (`/backend`) - Cấu trúc Django App
- `qlsv/`: Chứa file cấu hình gốc `settings.py` (cấu hình DB, App), `urls.py` (định tuyến root API). File `.env` lưu key bảo mật.
- `accounts/`, `students/`, `teachers/`, `academics/`: Đây là các Module (App). Trong mỗi App bạn sẽ làm việc với:
  - `models.py`: Nơi định nghĩa cấu trúc bảng CSDL (ORM).
  - `serializers.py`: Nơi định nghĩa format JSON trả về cho API.
  - `views.py` / `api.py`: Nơi viết logic API (ViewSets), xử lý lọc dữ liệu, phần quyền.
  - `urls.py`: Nơi khai báo Endpoint (Router).

### Frontend (`/frontend`) - Cấu trúc React Feature-based
- `package.json`: Chứa script start (`npm run dev`) và thư viện.
- `src/api/`: Nơi chứa cấu hình Axios (interceptors tự động gắn token vào header).
- `src/components/ui/`: Thư mục chứa các component atomic của `shadcn`. (Không nên sửa logic ở đây, chỉ đổi style nếu cần).
- `src/features/`: **Đây là nơi bạn sẽ code nhiều nhất.** Logic được gom theo tính năng (vd: `students`, `teachers`). Mỗi feature sẽ có `api.js` (gọi endpoint) và `hooks.js` (TanStack Query hooks).
- `src/pages/`: Các View ghép các component lại với nhau để tạo thành giao diện nguyên trang.

---

## 5. Lộ Trình Học Cấp Tốc Cho Thành Viên Mới (Accelerated Learning Path)

Để nhanh chóng nắm bắt hệ thống và commit code, bạn hãy theo sát lộ trình 4 bước sau:

**Bước 1: Django ORM & DRF (Backend - 2 ngày)**
- **Từ khóa cần học:** Django Models, QuerySet, ModelSerializer, ModelViewSet, DRF Permissions.
- *Thực hành:* Đọc hiểu file `academics/models.py`. Thử tạo một API mới đơn giản (ví dụ API đếm số lượng lớp học).

**Bước 2: React Core & Tailwind CSS (Frontend UI - 2 ngày)**
- **Từ khóa cần học:** Functional Component, `useState`, `useEffect`, Utility Classes của Tailwind.
- *Thực hành:* Tạo một Component tĩnh UI bằng Tailwind, thử sử dụng component Button, Input từ `shadcn/ui`.

**Bước 3: TanStack Query & Quản lý Form (Frontend Logic - 2 ngày)**
- **Từ khóa cần học:** `useQuery` (fetch data), `useMutation` (create/update data), React Hook Form, Zod schema validation.
- *Thực hành:* Viết code gọi API từ Bước 1 vào Component Bước 2, đổ dữ liệu ra giao diện. Thêm tính năng Search đơn giản.

**Bước 4: Authentication Flow (Ghép nối hệ thống - 1 ngày)**
- **Từ khóa cần học:** JWT Lifecycle, Axios Interceptors, Zustand state management.
- *Thực hành:* Đọc hiểu luồng đính kèm JWT vào request Header tại file cấu hình Axios của frontend.

---

## 6. Đánh Giá Hệ Thống & Gợi Ý Hướng Đi Tiếp Theo (Next Steps)

> [!IMPORTANT]
> **Nhận xét tổng quan:** Dự án đang có nền tảng kiến trúc rất tốt, tổ chức codebase sạch sẽ và sử dụng các công nghệ hiện đại bắt kịp xu hướng. Có test coverage cơ bản ở Backend.

### Nợ Kỹ Thuật (Technical Debt) & Điểm Cần Chú Ý
1. **Hiệu suất Database (N+1 Query Problem):** Do sử dụng ORM và DRF Serializer, nếu không cẩn thận khi query các bảng liên kết (ví dụ get danh sách `Classroom` kèm thông tin `Teacher`), API sẽ bắn ra hàng chục query nhỏ. Bạn cần luôn kiểm tra và sử dụng `select_related` / `prefetch_related` trong queryset của ViewSet.
2. **Authorization (Phân quyền):** Cần đảm bảo các ViewSet ở backend không chỉ có `IsAuthenticated` mà cần custom permission classes (vd: Sinh viên không được phép gọi method `DELETE` lớp học).
3. **Môi trường DB:** Đang dùng SQLite cho Test và PostgreSQL cho Prod. Điều này có thể gây lỗi tiềm ẩn (OperationalError) liên quan đến phân biệt chữ hoa/thường (Case-insensitive) hoặc date-time format.

### Đề Xuất Cải Tiến (Recommendations cho Phase tới)
- **Tối ưu hóa (Optimization):** Áp dụng Redis Caching cho các API danh mục (Khoa, Khóa, Môn học) vì các dữ liệu này ít thay đổi.
- **Bảo mật:** Rà soát lại việc xử lý refresh token, cân nhắc set `HttpOnly Cookies` thay vì lưu token trên client (localStorage) để chống tấn công XSS.
- **Tự động hóa (DevOps):** Thiết lập GitHub Actions Pipeline. Tự động chạy `pytest` và Frontend Linter (`eslint`) mỗi khi có Pull Request, ngăn chặn lỗi từ sớm.
- **Nghiệp vụ:** Xây dựng UI Frontend cho module Phân công giảng dạy (API Backend đã sẵn sàng). Trang bị tính năng tính Điểm Trung Bình (GPA) ở module `ExamResult`.
