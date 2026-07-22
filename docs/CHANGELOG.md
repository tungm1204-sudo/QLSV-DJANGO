# BẢN TIN CẬP NHẬT API (CHANGELOG) 📢

**Gửi Dev B (Frontend Team),**

Dựa trên feedback rất chính xác của bạn về việc *"Database ban đầu thiết kế quá đơn giản so với thực tế quản lý nhân sự tại trường Đại học"*, đội Backend đã tiến hành nâng cấp toàn bộ cấu trúc dữ liệu của module HR (Sinh viên, Giảng viên, Cán bộ). 

Dưới đây là chi tiết thay đổi để bạn có thể cập nhật lại Form UI trên Frontend.

## 📅 Ngày cập nhật: 23/07/2026 (Tích hợp Swagger - Giải cứu Frontend)

### 1. Báo tin vui cho Frontend Team! 🎉
Dựa trên những khó khăn của Dev B trong việc tích hợp API (phải tự đoán field, đọc code Backend), đội Backend đã tích hợp thành công **Swagger UI (OpenAPI 3.0)** vào hệ thống.

Từ nay, bạn **KHÔNG CẦN PHẢI ĐOÁN API NỮA**. 
Chỉ cần mở server backend lên và truy cập vào đường dẫn:
👉 **http://localhost:8000/api/docs/**

Tại đây, bạn sẽ thấy giao diện trực quan liệt kê TOÀN BỘ danh sách API, các tham số đầu vào (Request Body), và cấu trúc dữ liệu trả về (Response JSON). Bạn thậm chí có thể test gọi API trực tiếp trên giao diện này!

## 📅 Ngày cập nhật: 23/07/2026 (Fix N+1 Query & Cập nhật API AdministrativeClass)

### 1. Thêm mới API Quản lý Lớp hành chính (AdministrativeClass)
- **Vấn đề cũ:** Backend đã thiết kế bảng `Lớp hành chính` trong Database nhưng quên chưa publish API. Điều này gây khó khăn cho Frontend khi làm form "Thêm mới Sinh viên" vì không có API để lấy danh sách Lớp đổ vào thẻ `<select>`.
- **Giải pháp:** Đội Backend đã thêm đầy đủ API cho Lớp hành chính, bao gồm cả các trường tên liên kết để Frontend dễ hiển thị.
- **Endpoint mới:** 
  - `GET /api/v1/master-data/administrative-classes/` (Lấy danh sách, hỗ trợ search/filter)
  - `GET /api/v1/master-data/administrative-classes/{id}/` (Lấy chi tiết)
- **Cấu trúc JSON trả về mẫu:**
  ```json
  {
    "id": "uuid...",
    "code": "IT1",
    "name": "Công nghệ thông tin 1",
    "major_name": "Công nghệ thông tin",
    "cohort_name": "K64",
    "major": "uuid...",
    "cohort": "uuid...",
    "advisor": "uuid...",
    "is_active": true
  }
  ```
- **Tác vụ của Dev B:** Vui lòng sử dụng API này để render component Dropdown/Select danh sách Lớp hành chính khi tạo hoặc sửa thông tin Sinh viên nhé.

### 2. Sửa lỗi Crash API Khoa/Bộ môn (Department)
- **Vấn đề cũ:** Khi gọi `GET /api/v1/master-data/departments/`, API trả về lỗi `500 Internal Server Error`. Nguyên nhân do Backend query nhầm khóa ngoại `manager_id` (trường này thiết kế là tham chiếu lỏng UUID, không phải ForeignKey).
- **Giải pháp:** Đã gỡ bỏ đoạn query sai. API hiện tại đã hoạt động mượt mà trả về đúng mảng danh sách Khoa/Bộ môn.

### 3. Tối ưu dữ liệu trả về (Tránh N+1 Query)
- **Vấn đề cũ:** Ở các API như Lấy danh sách sinh viên (`GET /api/v1/hr/students/`), payload trước đây chỉ có mã ID của `education_system` hay `priority_category`. Dev B sẽ phải gọi thêm nhiều API lẻ tẻ để ánh xạ ra "Tên hệ đào tạo" hay "Tên đối tượng ưu tiên" để in ra màn hình.
- **Giải pháp:** Backend đã sử dụng `.select_related()` để JOIN trực tiếp dưới Database.
- **Kết quả (Tác vụ của Dev B):** 
  - Khi gọi các API get list của Sinh viên, Kế hoạch đào tạo, hay Lớp học phần, bạn sẽ thấy JSON trả về đã **tự động đính kèm thông tin chi tiết (nested) hoặc các trường tên (name)** của các bảng phụ.
  - Bạn **KHÔNG CẦN** gọi API phụ để map dữ liệu nữa, cứ chọc thẳng vào object JSON trả về để lấy text in ra UI. Form và Table của bạn sẽ load nhanh hơn đáng kể!

---

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
