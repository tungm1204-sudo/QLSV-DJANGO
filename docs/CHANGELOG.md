# BẢN TIN CẬP NHẬT API (CHANGELOG) 📢

**Gửi Dev B (Frontend Team),**

Dựa trên feedback rất chính xác của bạn về việc *"Database ban đầu thiết kế quá đơn giản so với thực tế quản lý nhân sự tại trường Đại học"*, đội Backend đã tiến hành nâng cấp toàn bộ cấu trúc dữ liệu của module HR (Sinh viên, Giảng viên, Cán bộ). 

Dưới đây là chi tiết thay đổi để bạn có thể cập nhật lại Form UI trên Frontend.

## 📅 Ngày cập nhật: 21/07/2026 (Update Module HR Sát Thực Tế)

### 1. Tại sao lại thay đổi?
File thiết kế `database.dbml` ban đầu chỉ cung cấp "khung xương" cơ bản. Khi đưa vào thực tế nghiệp vụ trường Đại học, việc thiếu các thông tin nhân khẩu học (Ngày sinh, Giới tính, Quê quán) hoặc thông tin tài chính (STK Ngân hàng, BHYT) sẽ gây lỗi dây chuyền cho các chức năng sau này (như xét học bổng, trả lương, báo cáo Bộ GD&ĐT). Do đó, Backend đã chủ động bổ sung để hệ thống linh hoạt và sát thực tế nhất.

### 2. Các trường dữ liệu (Fields) mới được bổ sung vào API
Khi bạn gọi API `GET /api/v1/hr/students/`, `GET /api/v1/hr/lecturers/`, hoặc `GET /api/v1/hr/staffs/`, JSON trả về sẽ có thêm rất nhiều field mới. **Tất cả các field mới đều cho phép null (optional)** nên sẽ không làm chết UI cũ của bạn.

#### 🧑‍🎓 API Sinh viên (Student)
- `date_of_birth`: Ngày sinh (YYYY-MM-DD).
- `gender`: Giới tính (`MALE`, `FEMALE`, `OTHER`).
- `place_of_birth`: Nơi sinh / Quê quán.
- `ethnicity`: Dân tộc (VD: Kinh, Tày...).
- `religion`: Tôn giáo.
- `nationality`: Quốc tịch.
- `personal_email`: Email cá nhân (Khác với email `.edu.vn` của trường).
- `permanent_address`: Hộ khẩu thường trú.
- `bank_account`: Số tài khoản ngân hàng.
- `health_insurance_number`: Mã thẻ BHYT.
- `education_system`: Hệ đào tạo (ID liên kết với Master Data).
- `priority_category`: Đối tượng ưu tiên (ID liên kết với Master Data).

#### 👨‍🏫 API Giảng viên (Lecturer) & Cán bộ (Staff)
- `date_of_birth`, `gender`, `place_of_birth`, `ethnicity`, `religion`, `nationality` (Như sinh viên).
- `id_card_number`: Số CMND / CCCD.
- `contact_phone`, `personal_email`, `address`.
- `bank_account`: STK Ngân hàng (Dùng để trả lương/thù lao).
- `degree`: Trình độ chuyên môn (Cử nhân, Thạc sĩ, Tiến sĩ).
- `join_date`: Ngày bắt đầu công tác.
- `status`: Trạng thái (`ACTIVE`, `RETIRED` - Nghỉ hưu, `RESIGNED` - Đã thôi việc).

### 3. Hành động cần làm từ phía Dev B
1. Đọc lại file `docs/database.dbml` (Đã được Backend cập nhật đồng bộ).
2. Thêm các trường nhập liệu tương ứng (Date picker cho Ngày sinh, Select cho Giới tính, Text input cho Quê quán, Ngân hàng...) vào form Tạo/Sửa Nhân sự trên Frontend.
3. Kéo code mới nhất từ nhánh `develop` về để API trả đúng format mới.

Cảm ơn bạn vì feedback cực kỳ giá trị giúp dự án hoàn thiện hơn! 🚀
