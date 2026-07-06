# TÀI LIỆU HƯỚNG DẪN DỰ ÁN & QUY TẮC PHÁT TRIỂN (RULES)

Tài liệu này đóng vai trò là "kim chỉ nam" cho toàn bộ thành viên trong nhóm phát triển Dự án Quản lý Sinh viên Đại học. Vui lòng đọc kỹ và tuân thủ nghiêm ngặt trong suốt quá trình xây dựng hệ thống.

---

## 1. TỔNG QUAN DỰ ÁN

- **Tên dự án:** Hệ thống Quản lý Sinh viên Đại học (Student Information System - SIS)
- **Mô tả:** Hệ thống quản lý toàn diện thông tin sinh viên, chương trình đào tạo, đăng ký học phần, điểm số, học phí, khen thưởng/kỷ luật và xét tốt nghiệp.
- **Tech Stack:**
  - **Frontend:** React 18+
  - **Backend:** Django 5.x, Django REST Framework (DRF) 3.15+
  - **Database:** NeonSQL (PostgreSQL 16+ Serverless)

### Sơ đồ luồng giao tiếp (Tổng quan)
```text
[User / Browser] 
       │ 
       ▼ 
[React Frontend] (Port 3000) 
       │ (REST API / JSON) 
       ▼ 
[Django DRF Backend] (Port 8000) 
       │ (Django ORM) 
       ▼ 
[NeonSQL Database] (PostgreSQL)
```

---

## 2. KIẾN TRÚC TRIỂN KHAI (MODULAR MONOLITH)

Hệ thống được xây dựng theo kiến trúc **Modular Monolith**. 

- **Cấu trúc Apps (Modules):** Các nghiệp vụ được phân tách thành các app: `students`, `courses`, `enrollment`, `users`, `grades`, `tuition`, `notifications`, `reports`...
- **Nguyên tắc giao tiếp:** 
  - Module A chỉ được phép gọi **Service** của Module B.
  - Tuyệt đối không được gọi trực tiếp Model, View hoặc Serializer của Module khác.

---

## 3. TỔ CHỨC MÃ NGUỒN (FEATURE-BASED)

### Cấu trúc Backend (Django)
```text
backend/
├── config/                 # Cấu hình gốc (settings, urls tổng)
├── apps/                   # Thư mục chứa các module nghiệp vụ
│   ├── identity/           # Quản lý người dùng, auth, phân quyền
│   ├── hr/                 # Quản lý hồ sơ sinh viên, giảng viên
│   ├── curriculum/         # Quản lý môn học, lớp học phần, ngành đào tạo
│   ├── enrollment/         # Đăng ký học phần, xếp thời khóa biểu
│   ├── exams/              # Khảo thí, lịch thi, phúc khảo
│   ├── finance/            # Học phí, miễn giảm, thanh toán
│   ├── affairs/            # Công tác sinh viên, học bổng
│   ├── notifications/      # Thông báo nội bộ
│   └── reports/            # Dashboard, báo cáo thống kê
├── shared/                 # Code dùng chung (Base models, mixins, utils)
└── requirements/           # Tách biệt dependencies (base, dev, prod)
```

### Cấu trúc Frontend (React)
- **Bắt buộc:** Toàn bộ logic code phải đặt trong thư mục `src/features/[feature-name]/`. 
- **Không vứt tất cả logic vào `pages/`.**

```text
frontend/src/
├── api/                # Cấu hình Axios
├── components/         # Shared components (Button, Table, Modal)
├── features/           # Feature-based modules (Chứa logic nghiệp vụ rạch ròi)
│   ├── auth/           
│   ├── hr/             
│   ├── curriculum/     
│   ├── enrollment/     
│   ├── finance/        
│   ├── master_data/    
│   ├── exams/          
│   ├── affairs/        
│   └── dashboard/      
├── hooks/              # Custom hooks dùng chung
├── routes/             # Setup React Router
└── utils/              # Helper functions
```

---

## 4. TỔ CHỨC NGHIỆP VỤ & QUY TẮC BACKEND (DJANGO)

Hệ thống áp dụng chặt chẽ pattern **Service Layer**:
- **Views:** Rất mỏng. Chỉ nhận HTTP Request, gọi Service, và trả về HTTP Response. **Tuyệt đối KHÔNG chứa business logic (như check điều kiện, tạo record).**
- **Services:** Rất dày. Chứa toàn bộ "Business Logic".
- **Selectors:** Nơi chứa các truy vấn DB phức tạp (Chuyên xử lý Query Read-only).
- **Models:** Thuần túy khai báo kiến trúc Database.

### Quy tắc tối thượng cho Backend:
1. **Database:** Khóa chính luôn là `UUIDField`. Mọi `ForeignKey` phải định nghĩa rõ `on_delete` (ưu tiên `RESTRICT`) và `related_name`.
2. **Transactions & Race Condition:** Mọi hành động ghi dữ liệu vào nhiều bảng (VD: Đăng ký môn + Tạo Hóa đơn) **BẮT BUỘC** dùng `@transaction.atomic` trong `services.py`. Sử dụng `select_for_update()` để chống Race Condition khi update số lượng (VD: Sĩ số lớp).
3. **Performance (N+1 Query):** Trong `selectors.py` hoặc `views.py`, mọi truy vấn lấy dữ liệu có ForeignKey bắt buộc phải dùng `.select_related()` hoặc `.prefetch_related()`.
4. **Viết Service:**
   - Validate nghiệp vụ trong Service.
   - Trả về Model instance hoặc Dict, không trả về `Response` của DRF.
   - Tuyệt đối không import View hoặc Serializer vào Service.

---

## 5. QUY TẮC FRONTEND (REACT)

1. **Data Fetching:** Bắt buộc sử dụng `@tanstack/react-query` cho mọi API GET/POST. **Tuyệt đối không dùng `useEffect` thuần để fetch data.**
2. **Form Management:** Bắt buộc sử dụng `react-hook-form` kết hợp `zod` để validate form.
3. **Component:** Sử dụng 100% Functional Components + Hooks.
4. **Global State:** Ưu tiên dùng Context API hoặc Zustand. (Không dùng Redux).
5. **State Handling:** Luôn có UI xử lý các trạng thái `Loading` và `Error` cho mọi API call.

---

## 6. GIAO TIẾP API (REST API)

- **Convention:** Dùng URL theo chuẩn: `/api/v1/{module}/{resource}/`.
- **Phân trang:** Mặc định `PageNumberPagination`, `page_size=20`.
- **Bảo mật API:** Sử dụng JWT (Access token 30 phút, Refresh token 7 ngày).
- **Rate Limiting:** 100 req/min (Authenticated), 20 req/min (Anonymous).

### HTTP Status Codes:
- **200:** Thành công / **201:** Tạo thành công.
- **400:** Lỗi validation / **422:** Lỗi định dạng data.
- **401:** Chưa xác thực / **403:** Không có quyền.
- **404:** Không tìm thấy.
- **409:** Xung đột dữ liệu (VD: Trùng lịch, sĩ số đầy).

---

## 7. QUY TẮC LÀM VIỆC NHÓM (GIT FLOW)

- **Nhánh chính:** `main` (Production), `develop` (Staging/Test).
- **Nhánh tính năng:** `feature/{module}/{mô-tả}` (VD: `feature/students/add-import`).
- **Commit Messages:** Tuân thủ Conventional Commits (`feat:`, `fix:`, `docs:`, `refactor:`).
- **Quy trình:** Tuyệt đối không Push trực tiếp lên `main` hay `develop`. Phải tạo Pull Request (PR) và có ít nhất 1 Approve.

---

## 8. KIỂM THỬ (TESTING)

- **Backend:** Dùng `pytest`. Bắt buộc có Unit Test cho `Service` và `Selector`. Coverage >= 80%.
- **Frontend:** Dùng `Vitest` + `React Testing Library`. Viết Integration Test cho các luồng quan trọng (Đăng ký học phần, Thanh toán).

---

## 9. BẢO MẬT & TRIỂN KHAI

- **Security:** Chống SQL Injection bằng ORM, chống XSS, validate mọi input, không commit `.env`.
- **Deploy:** Dockerize backend. Frontend serve tĩnh. Database sử dụng NeonSQL qua Connection Pooling. File uploads lưu trên AWS S3 / R2.
