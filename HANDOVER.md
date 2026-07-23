# Developer B Handover Notes (Identity Module)

## 1. Tổng quan hoàn thiện (Overview)
Trong những ngày qua, Module `identity` (Xác thực và Phân quyền - RBAC) đã được tái cấu trúc, hoàn thiện và kiểm thử kỹ lưỡng (End-to-End). Toàn bộ hệ thống hiện đã tuân thủ nghiêm ngặt mô hình Service Layer, tách bạch nghiệp vụ ra khỏi View và đảm bảo tiêu chuẩn bảo mật Enterprise.

## 2. Các chức năng và logic đã triển khai
### 2.1. Authentication & Security (Xác thực)
- **Cơ chế Khóa tài khoản (Lockout):** Đăng nhập sai 5 lần liên tiếp sẽ bị khóa tài khoản 15 phút (số lần và thời gian khóa đọc linh hoạt từ `SystemConfig`).
- **OTP Verification:** Tách biệt rõ ràng OTP dùng cho đăng nhập và OTP dùng cho lấy lại mật khẩu (`TypeChoices`), ngăn chặn tận dụng lỗ hổng dùng chéo OTP. OTP có thời hạn chặt chẽ (5 phút).
- **Bảo vệ phiên đăng nhập:** Triển khai tính năng Token Blacklisting (đưa token vào danh sách đen) khi Đăng xuất hoặc Khôi phục mật khẩu. Tự động vô hiệu hóa các phiên truy cập cũ (`LoginSession`).
- **Mật khẩu an toàn:** Giao diện đăng nhập và quên mật khẩu trên Frontend đã có tính năng Ẩn/Hiện mật khẩu, hỗ trợ Validation bằng Zod và hiển thị Toast Notification.

### 2.2. Role-Based Access Control (RBAC)
- **Role hệ thống (System Roles):** 6 vai trò mặc định (Administrator, Công tác SV, Giáo vụ, Giảng viên, Kế toán, Sinh viên) đã được khóa cứng bảo vệ. Admin không thể xóa hoặc sửa quyền của các role mặc định này.
- **Custom Roles:** Administrator có thể tạo/sửa/xóa linh hoạt các Role tùy chỉnh mới (VD: Trợ giảng) và tự gán quyền.
- **Phân quyền giao diện (UI) và API:**
  - **API Layer:** Mọi truy cập vào hệ thống đều được kiểm tra quyền hạn chặt chẽ ở lớp permission (trả về lỗi `403 Forbidden` nếu người dùng vượt quyền).
  - **UI Layer:** Nút bấm, hành động (Thêm/Sửa/Xóa) và các menu điều hướng (`Sidebar`) sẽ tự động bị mờ đi (disabled) hoặc ẩn hoàn toàn đối với user không đủ thẩm quyền, ngăn chặn thao tác sai ngay từ trên giao diện mà không cần đợi API báo lỗi.

### 2.3. Dọn dẹp & Tái cấu trúc Kiến trúc (Architecture Refactoring)
- Quy hoạch lại sự phụ thuộc của các module: Chuyển `SystemConfig` và `AuditLog` sang `core`, chuyển `Notification` sang `notifications` để giải phóng cho `identity`.
- Làm sạch schema Database: Các trường lưu UUID bằng text lỏng lẻo trước đây đã được chuyển hóa thành các `ForeignKey` chặt chẽ, tối ưu hiệu năng. Sơ đồ DB chuẩn nhất nằm ở `docs/database.dbml`.

## 3. Quy trình Kiểm thử đã thực hiện (Double Testing)
Toàn bộ tính năng đã được trải qua quy trình kiểm thử khắt khe ở hai cấp độ:
1. **Developer API Test:** Các kịch bản giả lập gọi API để tấn công hệ thống (như cố tình gọi endpoint khi không có quyền, spam đăng nhập sai) đều bị chặn thành công ở Backend.
2. **End-User UI Test:** Đã chạy thử nghiệm thực tế nghiệm thu trên Trình duyệt Web theo góc nhìn của một người dùng thông thường. Chức năng Search, Filter, Form Nhập liệu, hiển thị thông báo lỗi/thành công đều hoạt động mượt mà.

## 4. Test Credentials
Toàn bộ data rác đã được xóa. Lệnh `python manage.py setup_roles` đã tạo sẵn tài khoản cao nhất:
- **Email:** `admin@school.edu.vn`
- **Password:** `Password123!`
- **Role:** Administrator (Full toàn quyền)

Bạn hãy khởi động dự án bằng `python manage.py runserver` kết hợp `npm run dev` để bắt đầu!
