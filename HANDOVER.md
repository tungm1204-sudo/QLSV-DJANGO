# 🚀 TÀI LIỆU BÀN GIAO BACKEND CHO FRONTEND (DEV B)

**Hệ thống Quản lý Sinh viên (QLSV-DJANGO)** đã hoàn thiện 100% các API Backend đáp ứng trọn vẹn 9 Module theo yêu cầu (chi tiết trong `Module hệ thống QLSV.xlsx` và `FEATURE_CHECKLIST.md`).

Tài liệu này đóng vai trò hướng dẫn tích hợp và quy ước chung dành cho Frontend (Dev B) để bắt đầu công việc phát triển UI/UX.

---

## 1. Thông tin chung & Cấu hình môi trường
- **Công nghệ Backend**: Django REST Framework (Python 3)
- **Database**: PostgreSQL (NeonDB) - *Cấu hình đã lưu trong `.env`*
- **Base URL (Local)**: `http://localhost:8000/api/v1/`
- **Tài liệu API (Swagger/Redoc)**: 
  - Swagger UI: `http://localhost:8000/api/schema/swagger-ui/`
  - Redoc: `http://localhost:8000/api/schema/redoc/`
  *(Dev B bắt buộc sử dụng link Swagger này để lấy chính xác các Request Payload và Response Schema cho từng màn hình).*

---

## 2. Các Module Đã Hoàn Thiện (100% Phủ Sóng)
Toàn bộ **62 chức năng lớn** và hàng trăm sub-features của 9 Module dưới đây đã có API tương ứng:

1. **Module 1 (Hệ thống & Bảo mật):** Auth JWT, Phân quyền RBAC động, Audit Log, Cấu hình, Sao lưu/Phục hồi.
2. **Module 2 (Danh mục gốc):** Khoa/Ngành, Năm học, Khung đào tạo, Phòng học, Hình thức thi...
3. **Module 3 (Nhân sự):** Sinh viên, Giảng viên, Nhân viên, In thẻ sinh viên, Import hàng loạt.
4. **Module 4 (Đào tạo & Đăng ký môn):** Lên kế hoạch, TKB, Mở lớp, Đăng ký (Xử lý chống xung đột concurrency bằng khóa DB), Hủy lớp...
5. **Module 5 (Khảo thí & Điểm):** Xếp lịch thi, Nhập điểm (hệ 10), Tự động quy đổi sang hệ 4 & điểm chữ, Xét cảnh báo học vụ.
6. **Module 6 (CTSV):** Khen thưởng, Kỷ luật, Điểm rèn luyện, Khảo sát, BHYT.
7. **Module 7 (Tài chính & Học phí):** Cấu hình đơn giá, Sinh công nợ học phí tự động, Thu tiền, Hoàn tiền khi hủy môn.
8. **Module 8 (Xét Tốt nghiệp):** Check điều kiện tự động, Cấp phôi bằng, Đồ án/Khóa luận tốt nghiệp.
9. **Module 9 (Báo cáo & Thống kê):** Thống kê Dashboard, Xuất báo cáo PDF/Excel (Đào tạo, Tài chính, Điểm).

---

## 3. Quy ước Authentication & Authorization (Rất Quan Trọng)
Hệ thống sử dụng **JWT (JSON Web Token)** nhưng được quản lý chặt chẽ để chống XSS:
- **Quy trình đăng nhập:**
  1. Frontend gọi `POST /api/v1/identity/auth/login/` (Truyền `email` và `password`).
  2. Backend trả về `access` token trong body (Token sống 30 phút).
  3. Backend tự động set **`refresh_token` vào HttpOnly Cookie** (sống 7 ngày).
- **Gắn Access Token:** Mọi Request API cần quyền phải đính kèm Header:
  `Authorization: Bearer <access_token>`
- **Refresh Token (Tự động cấp lại token):** Khi `access_token` hết hạn (Backend báo `401 Unauthorized`), Frontend phải gọi ngầm:
  `POST /api/v1/identity/auth/refresh/` (Không cần truyền body, cookie sẽ tự gửi đi).
- **Phân quyền (RBAC):** Backend đã chặn quyền bằng HTTP Status `403 Forbidden`. Yêu cầu Frontend kiểm tra quyền của user (gọi `/users/me/`) để ẩn các nút bấm (Thêm/Sửa/Xóa) hoặc ẩn menu tương ứng để UX tốt hơn.

---

## 4. Các quy ước chuẩn (Conventions) cho Frontend

### 4.1. Pagination (Phân trang)
Các API danh sách mặc định có phân trang (10 record/page).
**Cấu trúc Response:**
```json
{
  "count": 100,
  "next": "http://localhost:8000/api/v1/hr/students/?page=2",
  "previous": null,
  "results": [ ...danh_sách_data... ]
}
```

### 4.2. Filtering & Searching
- **Tìm kiếm:** Gắn param `?search=keyword` để tìm text tổng hợp.
- **Lọc (Filter):** Truyền trực tiếp param theo ID hoặc trạng thái. Ví dụ: `?status=ACTIVE` hoặc `?major=123e4567-e89b-12d3-a456-426614174000`.
- **Sắp xếp (Ordering):** Truyền param `?ordering=created_at` (tăng dần) hoặc `?ordering=-created_at` (giảm dần).

### 4.3. Error Handling
Mọi lỗi được Backend chuẩn hóa chung:
```json
{
  "detail": "Mô tả lỗi tiếng Việt dành cho User/Frontend",
  "error_code": "Mã lỗi kỹ thuật (nếu có)"
}
```
Các mã HTTP bắt buộc phải xử lý:
- `400 Bad Request`: Lỗi validation (Ví dụ: Email không đúng định dạng).
- `401 Unauthorized`: Lỗi Token (hết hạn/chưa đăng nhập).
- `403 Forbidden`: Không có quyền thao tác (Ví dụ: Giảng viên cố xóa sinh viên).
- `404 Not Found`: Không tìm thấy ID đối tượng.
- `500 Internal Server Error`: Lỗi logic máy chủ (Backend).

---

## 5. Tài khoản Test Mặc định
Chạy Backend bằng lệnh `python manage.py runserver`, sau đó login bằng:
- **Email:** `admin@school.edu.vn`
- **Mật khẩu:** `Password123!`
- **Role:** Administrator (Có quyền tạo thêm user và test mọi module).

> **Lưu ý cuối:** Kiến trúc Backend đang sử dụng là **Thin Views - Fat Services** đảm bảo Transaction chặt chẽ và không có N+1 Queries. 
> Toàn bộ 20/20 kịch bản Unit Test cốt lõi đã chạy Pass. Chúc team UI/UX ráp giao diện suôn sẻ và rực rỡ! Có vấn đề gì về param hay dữ liệu mock, cứ nhắn Backend nhé! 🚀
