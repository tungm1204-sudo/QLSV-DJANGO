# Lộ Trình Phát Triển (Roadmap) - Các Giai Đoạn Tiếp Theo

Tài liệu này quy hoạch các tính năng sẽ được phát triển tiếp theo cho hệ thống **QLSV-DJANGO**. Việc tách tài liệu này giúp code base gọn gàng và bạn không cần phải đọc lại toàn bộ dự án từ đầu mỗi khi bắt đầu một Phase mới.

---

## ✅ Ngày 2 (Phase 6): Quản Lý Tài Chính & Học Phí (Đã hoàn thành)
**Mục tiêu:** Hệ thống tự động tính toán học phí dựa trên số tín chỉ môn học mà sinh viên đã ghi danh.

### Backend (Python/Django)
- Khởi tạo module/app mới: `finance` (hoặc gộp vào `academics`).
- **Models:** Tạo bảng `TuitionFee` (Sinh viên, Học kỳ, Tổng số tín chỉ, Số tiền phải nộp, Trạng thái: Chưa nộp / Đã nộp / Nợ).
- **Logic:** Tự động tính học phí: `Số tiền = Tổng tín chỉ * Đơn giá tín chỉ`. (Đơn giá tín chỉ sẽ cấu hình trong DB).
- **APIs:** `GET /api/finance/tuition/` (Admin xem toàn trường, Student xem của chính mình) và API `POST` cập nhật trạng thái thanh toán.

### Frontend (React)
- Xây dựng **Tuition Management Page**:
  - Dành cho Admin/Kế toán: Bảng thống kê tình hình thu học phí, lọc theo trạng thái (Nợ/Đã nộp), có nút "Xác nhận thu tiền".
  - Dành cho Sinh viên: Xem thông báo nợ học phí và chi tiết số tiền cần nộp.

---

## Ngày 3 (Phase 7): Báo Cáo Chuyên Sâu & Xuất PDF (Reporting)
**Mục tiêu:** Chuyên nghiệp hóa hệ thống văn bản và cung cấp góc nhìn phân tích cho Ban giám hiệu.

### Backend (Python/Django)
- Cài đặt thư viện `reportlab` hoặc `WeasyPrint`.
- Tạo API `GET /api/academics/export-transcript/`: Sinh ra **Bảng điểm cá nhân (PDF)** chuẩn form đại học có logo trường và điểm tổng kết.
- Cung cấp API `GET /api/academics/statistics/`: Tính toán dữ liệu Phổ điểm (tỉ lệ sinh viên đạt A, B, C, D) và tỉ lệ trượt/đỗ của từng học phần.

### Frontend (React)
- Thêm nút **Xuất Bảng Điểm (Download PDF)** tại trang kết quả học tập của Sinh viên.
- Nâng cấp **Dashboard Admin**: Thêm các biểu đồ phân tích (Bar chart/Pie chart) dựa trên dữ liệu thống kê phổ điểm vừa được cung cấp.

---

## Ngày 4 (Phase 8): Đăng Ký Tín Chỉ (Course Registration)
**Mục tiêu:** Thay vì Admin thêm sinh viên vào lớp bằng tay, sinh viên sẽ tự vào hệ thống "giành slot" đăng ký môn học đầu mỗi kỳ.

### Backend (Python/Django)
- **Models:** Thêm bảng `RegistrationPeriod` (Đợt đăng ký môn học, có Start Date & End Date).
- Giới hạn sĩ số (`max_students`) ở `Classroom` hoặc `Assignment`.
- **API (Transaction):** API xử lý hành động "Đăng ký":
  - Kiểm tra xem hiện tại có nằm trong Đợt đăng ký không?
  - Lớp đã full sĩ số chưa?
  - Có bị trùng lịch học không?
  - Nếu thỏa mãn, lưu vào `ClassroomStudent` (Sử dụng DB Transaction để tránh race condition khi hàng ngàn sinh viên truy cập cùng lúc).

### Frontend (React)
- Xây dựng **Course Registration Page (Trang Đăng Ký Tín Chỉ)** dành riêng cho Sinh viên:
  - Hiển thị thanh tiến trình (Ví dụ: "Bạn đã đăng ký 12/20 tín chỉ").
  - Hiển thị danh sách các lớp học phần đang mở. Sinh viên ấn "Đăng ký" -> UI cập nhật tức thời (hoặc báo lỗi nếu lớp đầy).
