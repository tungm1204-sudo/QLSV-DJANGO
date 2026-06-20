# PHẦN 1: TỔNG QUAN DỰ ÁN (PROJECT REPORT)

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
6. **Hệ thống Điểm danh (Attendance):** Đã hoàn thiện API (Filtering, Bulk Update, Attendance Sheet).
7. **API Phân công giảng dạy:** Backend API đã sẵn sàng với nested data (`classroom_name`, `course_name`, `teacher_name`) và hỗ trợ filter (`?classroom=`, `?course=`, `?teacher=`).

### 🚧 Đang thực hiện (Phase 3):
1. Hoàn thiện Form Thêm/Sửa cho Lớp sinh hoạt & Học phần.
2. Xây dựng giao diện Frontend (UI) cho module **Phân công giảng dạy** dựa trên API đã có.

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

## 7. Tài Liệu API & Kiến Thức Cốt Lõi (Knowledge Items)
Để tránh việc các lập trình viên và AI sau này phải "đọc lại toàn bộ code", dự án áp dụng hệ thống ghi nhớ và tài liệu hóa:
- **Tài liệu Walkthrough:** Bất cứ khi nào hoàn thành một tính năng, một bản báo cáo `walkthrough.md` sẽ được tạo ra để lưu trữ lại các endpoints mới (như Bulk Update Điểm danh). Bạn có thể tìm thấy trong lịch sử thay đổi của mình.
- **Báo cáo này (`PROJECT_REPORT.md` và `ONBOARDING_REPORT.md`):** Đóng vai trò là trí nhớ dài hạn (Long-term memory) chứa tóm tắt kiến trúc. Các AI mới khi join vào dự án có thể đọc file này để nắm ngay bối cảnh dự án thay vì tự scan source code.

---
> *Tài liệu cập nhật ngày: 08/06/2026 bởi Antigravity AI.*

## Cập nhật cleanup
- Repo đã được dọn sạch backend bằng cách loại bỏ file local và artifact không cần thiết.
- Thư mục `backend/core` hiện chỉ giữ lại cấu trúc cần thiết cho lệnh quản lý: `management/commands/setup_groups.py`.
- `.gitignore` đã được mở rộng để bỏ qua các file local `*.coverage` và `pytest_report.txt`.


---

# PHẦN 2: HƯỚNG DẪN ONBOARDING

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


---

# PHẦN 3: NHẬT KÝ PHÁT TRIỂN (CHANGELOG)

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

## 5. BẢO MẬT & DEVOPS (CẬP NHẬT MỚI)

1. **Bảo mật JWT Token**: Chuyển đổi phương thức lưu trữ `refresh_token` từ `localStorage` sang **HttpOnly Cookies**. Trình duyệt sẽ tự động đính kèm cookie này ở mỗi request refresh token mà không làm lộ token ra Javascript, ngăn chặn triệt để tấn công XSS. Backend đã được custom lại `CookieTokenRefreshView` và `LogoutView` để xử lý cookie.
2. **Phân quyền tuỳ chỉnh (Custom Permissions)**: Xây dựng các rules phân quyền dựa trên `Role` của user (Admin, Teacher, Student) trong file `accounts/permissions.py`. Ví dụ `IsAdminOrReadOnly` cho các API quản lý Khóa/Lớp, và `IsAdminOrTeacher` cho các API nhập điểm/điểm danh.
3. **Tối ưu Database**: Đã rà soát các ViewSet trong module Academics để thiết lập `select_related` và `prefetch_related`, dọn dẹp hoàn toàn vấn đề N+1 query.
4. **CI/CD Pipeline**: Tích hợp GitHub Actions Workflow (`ci.yml`) để tự động chạy kiểm thử cho Frontend (npm run lint) và Backend (pytest) mỗi khi có Push hoặc Pull Request.

---

## 6. HƯỚNG DẪN DÀNH CHO NGƯỜI VÀO SAU

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
