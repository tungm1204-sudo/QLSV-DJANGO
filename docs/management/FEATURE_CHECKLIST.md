# BẢNG THEO DÕI CHI TIẾT TỪNG TÍNH NĂNG (DỰA TRÊN EXCEL)

Sử dụng danh sách này làm Checklist (TODO) khi triển khai code cho từng Module để đảm bảo không bỏ sót bất kỳ tính năng nhỏ nào. Check `[x]` sau khi hoàn thành.


## MODULE 1: Hệ thống & Bảo mật

### Quản lý người dùng
- [x] **Tạo tài khoản mới (thủ công / import hàng loạt từ Excel)** - *Frontend: Form nhập liệu. Backend: Validate dữ liệu và insert (POST) vào CSDL.*
- [x] **Sửa thông tin tài khoản (email, SĐT, trạng thái)** - *Frontend: Form edit với dữ liệu cũ fill sẵn. Backend: Validate và update (PUT/PATCH) vào CSDL.*
- [x] **Khóa / mở khóa tài khoản** - *Backend: Khuyến nghị dùng Soft Delete (cập nhật cờ is_deleted/is_active) thay vì xóa cứng (DELETE) để bảo toàn khóa ngoại.*
- [x] **Gán vai trò cho tài khoản (Admin, Giáo vụ, Giảng viên, Sinh viên, Kế toán...)**
- [x] **Reset mật khẩu (do admin hoặc tự reset qua email/OTP)**
- [x] **Tìm kiếm, lọc danh sách tài khoản theo vai trò/trạng thái** - *Backend: Xây dựng API hỗ trợ query params (GET), kết hợp phân trang (Pagination).*
- [x] **Xem lịch sử đăng nhập của từng tài khoản**

### Phân quyền & Vai trò
- [x] **Tạo / sửa / xóa vai trò (role)** - *Frontend: Form nhập liệu. Backend: Validate dữ liệu và insert (POST) vào CSDL.*
- [x] **Gán quyền truy cập theo menu (ẩn/hiện menu theo vai trò)**
- [x] **Gán quyền CRUD chi tiết theo từng chức năng**
- [x] **Gán nhiều vai trò cho 1 tài khoản (nếu cần)**
- [x] **Ma trận phân quyền (role-permission matrix) để xem tổng quan**
- [x] **Sao chép cấu hình quyền từ vai trò có sẵn**

### Nhật ký hệ thống (Audit Log)
- [x] **Ghi log thao tác (tạo/sửa/xóa) kèm người thực hiện** - *Frontend: Form nhập liệu. Backend: Validate dữ liệu và insert (POST) vào CSDL.*
- [x] **Ghi nhận thời gian, địa chỉ IP, thiết bị truy cập**
- [x] **Tra cứu log theo người dùng, theo module, theo khoảng thời gian** - *Backend: Xây dựng API hỗ trợ query params (GET), kết hợp phân trang (Pagination).*
- [x] **Xuất log ra Excel/PDF phục vụ kiểm tra** - *Backend: Sử dụng thư viện xuất file (vd: pandas, reportlab) để trả về file từ query DB.*
- [x] **Cảnh báo hành vi bất thường (đăng nhập nhiều lần sai, sửa dữ liệu hàng loạt)** - *Frontend: Form edit với dữ liệu cũ fill sẵn. Backend: Validate và update (PUT/PATCH) vào CSDL.*

### Cấu hình hệ thống
- [x] **Cấu hình thông tin trường (tên, logo, địa chỉ, mã trường)**
- [x] **Cấu hình SMTP gửi email**
- [x] **Cấu hình gateway gửi SMS**
- [x] **Cấu hình thời gian khóa/mở nhập điểm theo học kỳ** - *Backend: Khuyến nghị dùng Soft Delete (cập nhật cờ is_deleted/is_active) thay vì xóa cứng (DELETE) để bảo toàn khóa ngoại.*
- [x] **Cấu hình tham số chung (năm học hiện hành, học kỳ hiện hành)**

### Sao lưu & Phục hồi
- [x] **Sao lưu dữ liệu tự động theo lịch (hằng ngày/tuần)**
- [x] **Sao lưu thủ công theo yêu cầu admin**
- [x] **Phục hồi dữ liệu từ bản sao lưu**
- [x] **Quản lý danh sách các bản sao lưu (xem, tải về, xóa)** - *Backend: Khuyến nghị dùng Soft Delete (cập nhật cờ is_deleted/is_active) thay vì xóa cứng (DELETE) để bảo toàn khóa ngoại.*
- [x] **Thông báo kết quả sao lưu (thành công/thất bại)**

### Xác thực & Bảo mật
- [x] **Đăng nhập bằng tài khoản/mật khẩu**
- [x] **Xác thực OTP qua email/SMS (2FA)**
- [x] **Khóa tài khoản tạm thời sau N lần đăng nhập sai** - *Backend: Khuyến nghị dùng Soft Delete (cập nhật cờ is_deleted/is_active) thay vì xóa cứng (DELETE) để bảo toàn khóa ngoại.*
- [x] **Quản lý phiên đăng nhập (session) — cho phép đăng xuất từ xa** - *Backend: Sử dụng thư viện xuất file (vd: pandas, reportlab) để trả về file từ query DB.*
- [x] **Chính sách mật khẩu (độ dài tối thiểu, ký tự đặc biệt, bắt buộc đổi định kỳ)**
- [x] **Quản lý thiết bị đã đăng nhập**

### Hệ thống Thông báo nội bộ
- [x] **Tạo và gửi thông báo thủ công (chọn người nhận theo vai trò/lớp/cá nhân)** - *Frontend: Form nhập liệu. Backend: Validate dữ liệu và insert (POST) vào CSDL.*
- [x] **Tự động hóa thông báo theo sự kiện hệ thống (System Triggers)** - *Kỹ thuật: Dùng cơ chế Event/Signals trong framework backend để trigger hành động gửi mà không làm nghẽn luồng xử lý chính.*
- [x] **Quản lý trạng thái thông báo (đã đọc/chưa đọc/đã xử lý)**
- [x] **Phân loại thông báo và bộ lọc tìm kiếm** - *Backend: Xây dựng API hỗ trợ query params (GET), kết hợp phân trang (Pagination).*
- [x] **Lịch sử thông báo đã gửi/nhận**

## MODULE 2: Quản lý danh mục gốc

### Danh mục đơn vị đào tạo
- [x] **Thêm/sửa/xóa Khoa, Bộ môn, Trung tâm** - *Frontend: Form nhập liệu. Backend: Validate dữ liệu và insert (POST) vào CSDL.*
- [x] **Quản lý cấu trúc phân cấp (Khoa → Bộ môn)**
- [x] **Gán trưởng/phó đơn vị**
- [x] **Trạng thái hoạt động/ngừng hoạt động của đơn vị**

### Danh mục ngành / chuyên ngành
- [x] **Thêm/sửa/xóa ngành đào tạo** - *Frontend: Form nhập liệu. Backend: Validate dữ liệu và insert (POST) vào CSDL.*
- [x] **Quản lý chuyên ngành trực thuộc ngành**
- [x] **Quản lý hệ đào tạo (Chính quy, Liên thông, Vừa làm vừa học...)** - *Frontend: Form nhập liệu. Backend: Validate dữ liệu và insert (POST) vào CSDL.*
- [x] **Gán ngành thuộc đơn vị (Khoa) quản lý**

### Danh mục khóa học & học kỳ
- [x] **Quản lý khóa tuyển sinh (VD: Khóa 2024-2028)** - *Backend: Khuyến nghị dùng Soft Delete (cập nhật cờ is_deleted/is_active) thay vì xóa cứng (DELETE) để bảo toàn khóa ngoại.*
- [x] **Quản lý năm học**
- [x] **Quản lý học kỳ (HK1, HK2, Hè) gắn với năm học**
- [x] **Thiết lập ngày bắt đầu/kết thúc học kỳ**

### Danh mục chương trình đào tạo
- [x] **Xây dựng khung chương trình đào tạo theo ngành/khóa** - *Frontend: Form nhập liệu. Backend: Validate dữ liệu và insert (POST) vào CSDL.*
- [x] **Thiết lập môn tiên quyết (prerequisite)** - *Logic: Phải join với bảng KQHT của học kỳ trước để xem sinh viên đã có điểm >= 5.0 (hoặc D) chưa.*
- [x] **Thiết lập học phần thay thế/tương đương**
- [x] **Quản lý số tín chỉ tối thiểu để tốt nghiệp**
- [x] **Sao chép chương trình đào tạo từ khóa trước** - *Frontend: Form nhập liệu. Backend: Validate dữ liệu và insert (POST) vào CSDL.*

### Danh mục môn học / học phần
- [x] **Thêm/sửa/xóa môn học (mã môn, tên môn)** - *Frontend: Form nhập liệu. Backend: Validate dữ liệu và insert (POST) vào CSDL.*
- [x] **Thiết lập số tín chỉ (lý thuyết, thực hành)**
- [x] **Phân loại học phần (bắt buộc, tự chọn, đại cương, chuyên ngành)**
- [x] **Quản lý đề cương môn học (tài liệu đính kèm)**

### Danh mục phòng học
- [x] **Thêm/sửa/xóa phòng học** - *Frontend: Form nhập liệu. Backend: Validate dữ liệu và insert (POST) vào CSDL.*
- [x] **Phân loại phòng (lý thuyết, thực hành, hội trường)**
- [x] **Thiết lập sức chứa từng phòng**
- [x] **Trạng thái sử dụng (đang dùng, bảo trì)**

### Danh mục hình thức thi
- [x] **Thêm/sửa các hình thức thi (viết, trắc nghiệm, vấn đáp, đồ án)** - *Frontend: Form nhập liệu. Backend: Validate dữ liệu và insert (POST) vào CSDL.*
- [x] **Thiết lập thang điểm tương ứng từng hình thức**
- [x] **Gán hình thức thi mặc định theo loại học phần**

### Danh mục đối tượng ưu tiên
- [x] **Thêm/sửa danh mục đối tượng ưu tiên (khu vực, chính sách, dân tộc...)** - *Frontend: Form nhập liệu. Backend: Validate dữ liệu và insert (POST) vào CSDL.*
- [x] **Thiết lập tỷ lệ/mức miễn giảm học phí tương ứng**
- [x] **Thiết lập điểm cộng ưu tiên (nếu áp dụng xét tuyển/học bổng)**

### Danh mục khen thưởng / kỷ luật
- [x] **Thêm/sửa các loại hình khen thưởng** - *Frontend: Form nhập liệu. Backend: Validate dữ liệu và insert (POST) vào CSDL.*
- [x] **Thêm/sửa các loại hình kỷ luật** - *Frontend: Form nhập liệu. Backend: Validate dữ liệu và insert (POST) vào CSDL.*
- [x] **Thiết lập điểm cộng/trừ rèn luyện tương ứng từng loại**
- [x] **Thiết lập mức độ kỷ luật (khiển trách, cảnh cáo, đình chỉ, buộc thôi học)**

### Quản lý Sinh viên
- [x] **Tạo hồ sơ sinh viên (thông tin cá nhân, liên hệ, gia đình)** - *(Hoàn thành Fullstack)* *Frontend: Form nhập liệu. Backend: Validate dữ liệu và insert (POST) vào CSDL.*

## MODULE 3: Quản lý nhân sự
- [x] **Import danh sách sinh viên hàng loạt từ Excel** - *(Hoàn thành Fullstack)* *Backend: Sử dụng thư viện xuất file (vd: pandas, reportlab) để trả về file từ query DB.*
- [x] **Cập nhật trạng thái học tập (đang học, bảo lưu, chuyển ngành, thôi học, tốt nghiệp)** - *(Hoàn thành Fullstack)* *Frontend: Form edit với dữ liệu cũ fill sẵn. Backend: Validate và update (PUT/PATCH) vào CSDL.*
- [x] **Quản lý lịch sử lớp học theo từng học kỳ** - *(Backend Done)*
- [x] **Tra cứu/tìm kiếm sinh viên theo nhiều tiêu chí** - *(Hoàn thành Fullstack)* *Backend: Xây dựng API hỗ trợ query params (GET), kết hợp phân trang (Pagination).*
- [x] **Quản lý ảnh đại diện và giấy tờ đính kèm (CCCD, học bạ...)** - *(Backend Done)*
- [x] **In thẻ sinh viên/giấy xác nhận** - *(Chưa làm UI In thẻ)*

### Quản lý Giảng viên
- [x] **Tạo hồ sơ giảng viên (thông tin cá nhân, học vị, học hàm)** - *(Backend Done)* *Frontend: Form nhập liệu. Backend: Validate dữ liệu và insert (POST) vào CSDL.*
- [x] **Quản lý chuyên môn/lĩnh vực giảng dạy** - *(Backend Done)*
- [x] **Quản lý lịch sử phân công giảng dạy** - *(Backend Done)*
- [x] **Quản lý hợp đồng/biên chế (cơ hữu, thỉnh giảng)** - *(Backend Done)*
- [x] **Tra cứu giảng viên theo khoa/bộ môn/chuyên môn** - *(Backend Done)* *Backend: Xây dựng API hỗ trợ query params (GET), kết hợp phân trang (Pagination).*

### Quản lý Cán bộ - Nhân viên
- [x] **Tạo hồ sơ nhân viên (giáo vụ, kế toán, thư viện, hành chính)** - *(Backend Done)* *Frontend: Form nhập liệu. Backend: Validate dữ liệu và insert (POST) vào CSDL.*
- [x] **Phân loại theo bộ phận/phòng ban** - *(Backend Done)*
- [x] **Quản lý chức vụ, nhiệm vụ phụ trách** - *(Backend Done)*
- [x] **Tra cứu/tìm kiếm nhân viên** - *(Backend Done)* *Backend: Xây dựng API hỗ trợ query params (GET), kết hợp phân trang (Pagination).*

### Phân công giảng dạy
- [x] **Gán giảng viên phụ trách cho từng lớp học phần**
- [x] **Kiểm tra trùng lịch giảng dạy của giảng viên** - *Nghiệp vụ: So sánh Ca học + Ngày học + Phòng học/Giảng viên. Kỹ thuật: Query check Overlap Time trong SQL.*
- [x] **Thống kê khối lượng giờ giảng theo giảng viên/học kỳ**
- [x] **Điều chỉnh/thay đổi giảng viên phụ trách giữa kỳ**

### Kế hoạch đào tạo năm học
- [x] **Lập kế hoạch mở môn học theo từng học kỳ/năm học**

## MODULE 4: Kế hoạch & Đăng ký học phần
- [x] **Dự kiến số lớp, sĩ số mỗi môn** - *Database: Sử dụng Transaction và row-level locking (select_for_update) để chống xung đột (concurrency).*
- [x] **Phê duyệt kế hoạch đào tạo (workflow duyệt)** - *Frontend: Form nhập liệu. Backend: Validate dữ liệu và insert (POST) vào CSDL.*
- [x] **Sao chép kế hoạch từ học kỳ trước để điều chỉnh**

### Xây dựng thời khóa biểu
- [x] **Xếp lịch học theo phòng/giảng viên/thời gian**
- [x] **Kiểm tra trùng lịch (phòng, giảng viên, lớp)** - *Nghiệp vụ: So sánh Ca học + Ngày học + Phòng học/Giảng viên. Kỹ thuật: Query check Overlap Time trong SQL.*
- [x] **Xếp lịch thi sơ bộ**
- [x] **Xuất thời khóa biểu theo lớp/giảng viên/phòng** - *Backend: Khuyến nghị dùng Soft Delete (cập nhật cờ is_deleted/is_active) thay vì xóa cứng (DELETE) để bảo toàn khóa ngoại.*
- [x] **Điều chỉnh thời khóa biểu khi có thay đổi** - *Backend: Khuyến nghị dùng Soft Delete (cập nhật cờ is_deleted/is_active) thay vì xóa cứng (DELETE) để bảo toàn khóa ngoại.*

### Mở lớp học phần
- [x] **Tạo lớp học phần từ học phần trong chương trình đào tạo** - *Frontend: Form nhập liệu. Backend: Validate dữ liệu và insert (POST) vào CSDL.*
- [x] **Thiết lập giới hạn sĩ số tối đa/tối thiểu** - *Database: Sử dụng Transaction và row-level locking (select_for_update) để chống xung đột (concurrency).*
- [x] **Thiết lập điều kiện đăng ký (đã học môn tiên quyết...)** - *Logic: Phải join với bảng KQHT của học kỳ trước để xem sinh viên đã có điểm >= 5.0 (hoặc D) chưa.*
- [x] **Đóng/hủy lớp học phần nếu không đủ sĩ số** - *Database: Sử dụng Transaction và row-level locking (select_for_update) để chống xung đột (concurrency).*

### Đăng ký học phần
- [x] **Sinh viên xem danh sách lớp học phần mở trong kỳ**
- [x] **Đăng ký học phần online**
- [x] **Hệ thống tự kiểm tra điều kiện (môn tiên quyết, số tín chỉ tối đa)** - *Logic: Phải join với bảng KQHT của học kỳ trước để xem sinh viên đã có điểm >= 5.0 (hoặc D) chưa.*
- [x] **Hệ thống tự kiểm tra xung đột lịch học** - *Nghiệp vụ: So sánh Ca học + Ngày học + Phòng học/Giảng viên. Kỹ thuật: Query check Overlap Time trong SQL.*
- [x] **Xác nhận đăng ký thành công, xem phiếu đăng ký**

### Đăng ký ngoài kế hoạch
- [x] **Đăng ký học lại (môn không đạt)**
- [x] **Đăng ký học cải thiện điểm**
- [x] **Đăng ký học vượt (vượt tiến độ)**
- [x] **Phê duyệt các trường hợp đăng ký đặc biệt**

### Danh sách lớp chính thức
- [x] **Chốt danh sách sinh viên sau thời gian đăng ký/điều chỉnh**
- [x] **Đồng bộ danh sách sang module điểm danh**
- [x] **Xuất danh sách lớp (file Excel/PDF) cho giảng viên** - *Backend: Sử dụng thư viện xuất file (vd: pandas, reportlab) để trả về file từ query DB.*
- [x] **Khóa danh sách, không cho chỉnh sửa sau khi chốt** - *Frontend: Form edit với dữ liệu cũ fill sẵn. Backend: Validate và update (PUT/PATCH) vào CSDL.*

### Điều chỉnh đăng ký
- [x] **Hủy đăng ký học phần trong thời gian quy định**
- [x] **Đổi lớp học phần (chuyển từ lớp này sang lớp khác)**
- [x] **Giới hạn thời gian được phép điều chỉnh**
- [x] **Lưu lịch sử các lần điều chỉnh**

### Lập lịch thi
- [x] **Xếp lịch thi theo môn/lớp học phần**

## MODULE 5: Khảo thí & Quản lý điểm
- [x] **Xếp phòng thi, gán số lượng sinh viên/phòng**
- [x] **Gán cán bộ coi thi (giám thị)**
- [x] **Thiết lập hình thức thi cho từng kỳ thi**
- [x] **Xuất lịch thi cho sinh viên/giảng viên** - *Backend: Sử dụng thư viện xuất file (vd: pandas, reportlab) để trả về file từ query DB.*

### Nhập điểm thành phần
- [x] **Nhập điểm chuyên cần**
- [x] **Nhập điểm giữa kỳ**
- [x] **Nhập điểm thực hành/bài tập**
- [x] **Thiết lập trọng số (%) từng thành phần**
- [x] **Import điểm hàng loạt từ Excel** - *Backend: Sử dụng thư viện xuất file (vd: pandas, reportlab) để trả về file từ query DB.*

### Nhập điểm cuối kỳ
- [x] **Nhập điểm thi cuối kỳ**
- [x] **Khóa điểm sau thời hạn quy định (không cho sửa)** - *Frontend: Form edit với dữ liệu cũ fill sẵn. Backend: Validate và update (PUT/PATCH) vào CSDL.*
- [x] **Giảng viên gửi yêu cầu mở khóa điểm khi cần chỉnh sửa** - *Frontend: Form edit với dữ liệu cũ fill sẵn. Backend: Validate và update (PUT/PATCH) vào CSDL.*
- [x] **Lịch sử thay đổi điểm (ai sửa, khi nào)** - *Frontend: Form edit với dữ liệu cũ fill sẵn. Backend: Validate và update (PUT/PATCH) vào CSDL.*

### Tính điểm tổng kết
- [x] **Tự động tính điểm tổng kết học phần theo trọng số**
- [x] **Quy đổi điểm hệ 10 sang hệ 4 và điểm chữ (A, B, C...)** - *Nghiệp vụ: Áp dụng công thức (Tổng điểm * Số tín chỉ)/Tổng tín chỉ. Cần chạy background task hoặc tính lại mỗi khi điểm thay đổi.*
- [x] **Tính điểm trung bình học kỳ (GPA kỳ)**
- [x] **Tính điểm trung bình tích lũy (CPA)**
- [x] **Xếp loại học lực theo điểm trung bình**

### Phúc khảo
- [x] **Sinh viên gửi đơn phúc khảo online**
- [x] **Giáo vụ tiếp nhận, phân công chấm phúc khảo**
- [x] **Cập nhật kết quả phúc khảo (giữ nguyên/thay đổi điểm)** - *Frontend: Form edit với dữ liệu cũ fill sẵn. Backend: Validate và update (PUT/PATCH) vào CSDL.*
- [x] **Thông báo kết quả phúc khảo cho sinh viên**

### Bảng điểm
- [x] **Tra cứu điểm theo từng học kỳ** - *Backend: Xây dựng API hỗ trợ query params (GET), kết hợp phân trang (Pagination).*
- [x] **Tra cứu điểm tích lũy toàn khóa** - *Backend: Khuyến nghị dùng Soft Delete (cập nhật cờ is_deleted/is_active) thay vì xóa cứng (DELETE) để bảo toàn khóa ngoại.*
- [x] **Xuất bảng điểm (PDF) có xác nhận của trường** - *Backend: Sử dụng thư viện xuất file (vd: pandas, reportlab) để trả về file từ query DB.*
- [x] **In bảng điểm tạm thời/chính thức**

### Cảnh báo học vụ
- [x] **Tự động phát hiện sinh viên có GPA dưới ngưỡng**
- [x] **Phát hiện sinh viên nợ môn vượt mức quy định**
- [x] **Gửi thông báo cảnh báo học vụ tới sinh viên/cố vấn**
- [x] **Theo dõi danh sách sinh viên bị cảnh báo qua các kỳ**

### Điểm rèn luyện
- [x] **Sinh viên tự đánh giá điểm rèn luyện (nếu áp dụng)**

## MODULE 6: Công tác sinh viên & Rèn luyện
- [x] **Lớp/cố vấn xét duyệt điểm rèn luyện**
- [x] **Tính điểm và xếp loại rèn luyện theo kỳ**
- [x] **Tra cứu lịch sử điểm rèn luyện qua các kỳ** - *Backend: Xây dựng API hỗ trợ query params (GET), kết hợp phân trang (Pagination).*

### Khen thưởng - Kỷ luật
- [x] **Lập và quản lý quyết định khen thưởng (theo danh mục)**
- [x] **Lập và quản lý quyết định kỷ luật**
- [x] **Đính kèm văn bản quyết định**
- [x] **Tra cứu lịch sử khen thưởng/kỷ luật theo sinh viên** - *Backend: Xây dựng API hỗ trợ query params (GET), kết hợp phân trang (Pagination).*

### Học bổng
- [x] **Thiết lập tiêu chí xét học bổng (theo GPA, rèn luyện, hoàn cảnh)**
- [x] **Lập danh sách sinh viên đủ điều kiện xét**
- [x] **Phê duyệt danh sách nhận học bổng**
- [x] **Thông báo kết quả học bổng**

### Cố vấn học tập
- [x] **Phân công cố vấn học tập cho từng lớp/sinh viên**
- [x] **Ghi nhận nội dung tư vấn, buổi gặp**
- [x] **Cố vấn xem được tình hình học tập của sinh viên phụ trách**
- [x] **Lịch sử các lần tư vấn**

### Khảo sát sinh viên
- [x] **Tạo phiếu khảo sát (đánh giá môn học, giảng viên)** - *Frontend: Form nhập liệu. Backend: Validate dữ liệu và insert (POST) vào CSDL.*
- [x] **Sinh viên thực hiện khảo sát online**
- [x] **Tổng hợp kết quả khảo sát theo môn/giảng viên**
- [x] **Xuất báo cáo khảo sát** - *Backend: Sử dụng thư viện xuất file (vd: pandas, reportlab) để trả về file từ query DB.*

### Bảo hiểm y tế
- [x] **Quản lý danh sách sinh viên tham gia BHYT**
- [x] **Theo dõi thời hạn tham gia/hết hạn**
- [x] **Ghi nhận thanh toán phí BHYT**
- [x] **Xuất danh sách báo cáo BHYT theo lớp/khóa** - *Backend: Khuyến nghị dùng Soft Delete (cập nhật cờ is_deleted/is_active) thay vì xóa cứng (DELETE) để bảo toàn khóa ngoại.*

### Thiết lập học phí
- [x] **Cấu hình đơn giá học phí theo tín chỉ**

## MODULE 7: Tài chính & Học phí
- [x] **Thiết lập mức học phí riêng theo ngành/hệ đào tạo (nếu khác nhau)** - *Frontend: Form nhập liệu. Backend: Validate dữ liệu và insert (POST) vào CSDL.*
- [x] **Cập nhật đơn giá theo từng năm học** - *Frontend: Form edit với dữ liệu cũ fill sẵn. Backend: Validate và update (PUT/PATCH) vào CSDL.*

### Tính công nợ
- [x] **Tự động sinh công nợ học phí dựa trên đăng ký học phần** - *Nghiệp vụ: Tự động chốt công nợ vào đầu kỳ. Kỹ thuật: Cần có liên kết (ForeignKey) chuẩn xác tới bảng Đăng ký học phần để đếm số tín chỉ.*
- [x] **Theo dõi tình trạng công nợ (đã đóng, còn nợ, quá hạn)**
- [x] **Gửi thông báo nhắc nợ tự động** - *Kỹ thuật: Dùng cơ chế Event/Signals trong framework backend để trigger hành động gửi mà không làm nghẽn luồng xử lý chính.*
- [x] **Tự động hoàn trả học phí/công nợ cho sinh viên khi lớp học phần bị hủy**
- [x] **Tổng hợp công nợ theo lớp/khóa/sinh viên** - *Backend: Khuyến nghị dùng Soft Delete (cập nhật cờ is_deleted/is_active) thay vì xóa cứng (DELETE) để bảo toàn khóa ngoại.*

### Quản lý phiếu thu
- [x] **Lập phiếu thu học phí**
- [x] **In biên lai thu tiền**
- [x] **Ghi nhận hình thức thanh toán (tiền mặt, chuyển khoản, online)**
- [x] **Tra cứu lịch sử thanh toán theo sinh viên** - *Backend: Xây dựng API hỗ trợ query params (GET), kết hợp phân trang (Pagination).*

### Miễn giảm & Gia hạn
- [x] **Lập hồ sơ xét miễn giảm học phí (theo đối tượng ưu tiên)**
- [x] **Phê duyệt miễn giảm**
- [x] **Gia hạn thời gian đóng học phí**
- [x] **Theo dõi danh sách sinh viên được miễn giảm/gia hạn**

### Tài khoản ngân hàng
- [x] **Kết nối cổng thanh toán trực tuyến (VNPay, Momo, ngân hàng...)**
- [x] **Đối soát giao dịch thanh toán tự động** - *Database: Sử dụng Transaction và row-level locking (select_for_update) để chống xung đột (concurrency).*
- [x] **Xử lý giao dịch lỗi/hoàn tiền** - *Database: Sử dụng Transaction và row-level locking (select_for_update) để chống xung đột (concurrency).*
- [x] **Lịch sử giao dịch qua cổng thanh toán** - *Database: Sử dụng Transaction và row-level locking (select_for_update) để chống xung đột (concurrency).*

### Quản lý hoàn trả / Giảm trừ
- [x] **Tự động hoàn trả/giảm trừ công nợ khi lớp học phần bị hủy.** - *Logic sẽ kích hoạt (Trigger) ngay khi trạng thái lớp ở Module 4 chuyển thành "Hủy". Hệ thống bắt buộc phải sử dụng Transaction trong Database để đảm bảo tiền/tín chỉ được hoàn về tài khoản sinh viên đồng bộ với việc xóa tên khỏi danh sách lớp, tránh thất thoát dữ liệu.*

## MODULE 8: Thẩm định & Xét tốt nghiệp

### Điều kiện tốt nghiệp
- [x] **Thiết lập điều kiện tốt nghiệp theo ngành (tín chỉ, GPA, chứng chỉ, rèn luyện...)**
- [x] **Cấu hình điều kiện theo từng khóa (có thể khác nhau)** - *Backend: Khuyến nghị dùng Soft Delete (cập nhật cờ is_deleted/is_active) thay vì xóa cứng (DELETE) để bảo toàn khóa ngoại.*

### Kiểm tra điều kiện
- [x] **Đối chiếu tự động điều kiện tốt nghiệp với hồ sơ từng sinh viên**
- [x] **Hiển thị danh sách điều kiện còn thiếu (nếu có)**
- [x] **Sinh viên tự tra cứu tiến độ đủ điều kiện tốt nghiệp** - *Backend: Xây dựng API hỗ trợ query params (GET), kết hợp phân trang (Pagination).*

### Danh sách xét tốt nghiệp
- [x] **Lập danh sách sinh viên đủ điều kiện theo đợt xét**
- [x] **Trình hội đồng phê duyệt danh sách**
- [x] **Công bố danh sách chính thức được công nhận tốt nghiệp**

### Quản lý phôi bằng
- [x] **Quản lý số lượng phôi bằng tồn/đã sử dụng**
- [x] **In bằng tốt nghiệp**
- [x] **In bảng điểm toàn khóa kèm theo bằng** - *Backend: Khuyến nghị dùng Soft Delete (cập nhật cờ is_deleted/is_active) thay vì xóa cứng (DELETE) để bảo toàn khóa ngoại.*
- [x] **Quản lý số hiệu, số vào sổ cấp bằng**

### Hồ sơ tốt nghiệp
- [x] **Theo dõi tình trạng nhận bằng của từng sinh viên**
- [x] **Ghi nhận ngày nhận bằng, người nhận thay (nếu có ủy quyền)**
- [x] **Lưu trữ hồ sơ tốt nghiệp điện tử**

### Xét tốt nghiệp sớm / muộn
- [x] **Xử lý trường hợp sinh viên chuyển trường**
- [x] **Xử lý trường hợp chương trình đào tạo thay đổi giữa khóa học** - *Frontend: Form nhập liệu. Backend: Validate dữ liệu và insert (POST) vào CSDL.*
- [x] **Xử lý trường hợp sinh viên bị kỷ luật/đình chỉ ảnh hưởng tốt nghiệp**
- [x] **Xét đặc cách/đặc biệt theo quy định riêng**

### Quản lý Đồ án & Thẩm định Tốt nghiệp
- [x] **Đăng ký đề tài đồ án/khóa luận tốt nghiệp** - *Backend: Khuyến nghị dùng Soft Delete (cập nhật cờ is_deleted/is_active) thay vì xóa cứng (DELETE) để bảo toàn khóa ngoại.*
- [x] **Phân công giảng viên hướng dẫn**
- [x] **Phân công giảng viên phản biện**
- [x] **Thành lập hội đồng bảo vệ (thành viên, chủ tịch, thư ký)**
- [x] **Lên lịch bảo vệ**
- [x] **Chấm điểm khóa luận/đồ án (điểm hướng dẫn, phản biện, hội đồng)** - *Backend: Khuyến nghị dùng Soft Delete (cập nhật cờ is_deleted/is_active) thay vì xóa cứng (DELETE) để bảo toàn khóa ngoại.*
- [x] **Tổng hợp kết quả bảo vệ**

### Chuyển đổi tín chỉ & Học phần tương đương
- [x] **Thiết lập bộ quy tắc môn học tương đương (Mapping Rules) giữa các ngành.**
- [x] **Ánh xạ (Map) kết quả học tập từ khung chương trình cũ sang khung mới. Clone bản ghi điểm để bảo toàn lịch sử thay vì sửa trực tiếp.**
- [x] **Tự động loại bỏ các môn không tương đương (chuyển thành môn ngoài khung), tách chúng khỏi thuật toán tính GPA của ngành mới.**

## MODULE 9: Thống kê & Báo cáo

### Dashboard
- [x] **Biểu đồ tổng quan số lượng sinh viên (theo khóa/ngành/trạng thái)** - *Backend: Khuyến nghị dùng Soft Delete (cập nhật cờ is_deleted/is_active) thay vì xóa cứng (DELETE) để bảo toàn khóa ngoại.*
- [x] **Biểu đồ tổng quan tình hình học phí (đã thu/còn nợ)**
- [x] **Biểu đồ tổng quan đào tạo (số lớp, số môn mở trong kỳ)** - *Frontend: Form nhập liệu. Backend: Validate dữ liệu và insert (POST) vào CSDL.*
- [x] **Tùy chỉnh widget hiển thị theo vai trò người dùng**

### Báo cáo đào tạo
- [x] **Thống kê số lượng sinh viên theo khoa/ngành/khóa** - *Backend: Khuyến nghị dùng Soft Delete (cập nhật cờ is_deleted/is_active) thay vì xóa cứng (DELETE) để bảo toàn khóa ngoại.*
- [x] **Thống kê số lớp học phần mở theo học kỳ**
- [x] **Xuất báo cáo theo nhiều định dạng** - *Backend: Sử dụng thư viện xuất file (vd: pandas, reportlab) để trả về file từ query DB.*

### Báo cáo học tập
- [x] **Thống kê học lực sinh viên (giỏi, khá, trung bình, yếu)**
- [x] **Thống kê tỷ lệ đạt/trượt theo môn học**
- [x] **Thống kê theo lớp/khóa/ngành** - *Backend: Khuyến nghị dùng Soft Delete (cập nhật cờ is_deleted/is_active) thay vì xóa cứng (DELETE) để bảo toàn khóa ngoại.*

### Báo cáo tài chính
- [x] **Tổng hợp số liệu thu học phí theo kỳ/năm**
- [x] **Tổng hợp công nợ còn tồn đọng**
- [x] **Báo cáo doanh thu theo khoa/ngành**

### Báo cáo nhân sự
- [x] **Thống kê số lượng giảng viên theo khoa/bộ môn**
- [x] **Thống kê giờ giảng theo giảng viên/học kỳ**
- [x] **Báo cáo khối lượng công tác**

### Báo cáo khảo thí
- [x] **Thống kê lịch thi đã tổ chức**
- [x] **Thống kê kết quả thi theo môn/lớp**
- [x] **Báo cáo tỷ lệ phúc khảo và kết quả phúc khảo**

### Báo cáo tùy chỉnh
- [x] **Cho phép người dùng tự chọn tiêu chí, cột dữ liệu để xuất báo cáo** - *Backend: Sử dụng thư viện xuất file (vd: pandas, reportlab) để trả về file từ query DB.*
- [x] **Xuất báo cáo ra Excel** - *Backend: Sử dụng thư viện xuất file (vd: pandas, reportlab) để trả về file từ query DB.*
- [x] **Xuất báo cáo ra PDF** - *Backend: Sử dụng thư viện xuất file (vd: pandas, reportlab) để trả về file từ query DB.*
- [x] **Lưu mẫu báo cáo đã tùy chỉnh để dùng lại**

### Xuất dữ liệu
- [x] **Xuất dữ liệu sinh viên/điểm/tốt nghiệp theo mẫu chuẩn của Bộ GD&ĐT** - *Backend: Sử dụng thư viện xuất file (vd: pandas, reportlab) để trả về file từ query DB.*
- [x] **Kiểm tra tính hợp lệ dữ liệu trước khi xuất** - *Backend: Sử dụng thư viện xuất file (vd: pandas, reportlab) để trả về file từ query DB.*
- [x] **Lưu lịch sử các lần xuất dữ liệu** - *Backend: Sử dụng thư viện xuất file (vd: pandas, reportlab) để trả về file từ query DB.*
