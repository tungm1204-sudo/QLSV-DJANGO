# BẢNG THEO DÕI CHI TIẾT TỪNG TÍNH NĂNG (DỰA TRÊN EXCEL)

Sử dụng danh sách này làm Checklist (TODO) khi triển khai code cho từng Module để đảm bảo không bỏ sót bất kỳ tính năng nhỏ nào. Check `[x]` sau khi hoàn thành.


## MODULE 1: Hệ thống & Bảo mật

### Quản lý người dùng
- [ ] **Tạo tài khoản mới (thủ công / import hàng loạt từ Excel)** - *Frontend: Form nhập liệu. Backend: Validate dữ liệu và insert (POST) vào CSDL.*
- [ ] **Sửa thông tin tài khoản (email, SĐT, trạng thái)** - *Frontend: Form edit với dữ liệu cũ fill sẵn. Backend: Validate và update (PUT/PATCH) vào CSDL.*
- [ ] **Khóa / mở khóa tài khoản** - *Backend: Khuyến nghị dùng Soft Delete (cập nhật cờ is_deleted/is_active) thay vì xóa cứng (DELETE) để bảo toàn khóa ngoại.*
- [ ] **Gán vai trò cho tài khoản (Admin, Giáo vụ, Giảng viên, Sinh viên, Kế toán...)**
- [ ] **Reset mật khẩu (do admin hoặc tự reset qua email/OTP)**
- [ ] **Tìm kiếm, lọc danh sách tài khoản theo vai trò/trạng thái** - *Backend: Xây dựng API hỗ trợ query params (GET), kết hợp phân trang (Pagination).*
- [ ] **Xem lịch sử đăng nhập của từng tài khoản**

### Phân quyền & Vai trò
- [ ] **Tạo / sửa / xóa vai trò (role)** - *Frontend: Form nhập liệu. Backend: Validate dữ liệu và insert (POST) vào CSDL.*
- [ ] **Gán quyền truy cập theo menu (ẩn/hiện menu theo vai trò)**
- [ ] **Gán quyền CRUD chi tiết theo từng chức năng**
- [ ] **Gán nhiều vai trò cho 1 tài khoản (nếu cần)**
- [ ] **Ma trận phân quyền (role-permission matrix) để xem tổng quan**
- [ ] **Sao chép cấu hình quyền từ vai trò có sẵn**

### Nhật ký hệ thống (Audit Log)
- [ ] **Ghi log thao tác (tạo/sửa/xóa) kèm người thực hiện** - *Frontend: Form nhập liệu. Backend: Validate dữ liệu và insert (POST) vào CSDL.*
- [ ] **Ghi nhận thời gian, địa chỉ IP, thiết bị truy cập**
- [ ] **Tra cứu log theo người dùng, theo module, theo khoảng thời gian** - *Backend: Xây dựng API hỗ trợ query params (GET), kết hợp phân trang (Pagination).*
- [ ] **Xuất log ra Excel/PDF phục vụ kiểm tra** - *Backend: Sử dụng thư viện xuất file (vd: pandas, reportlab) để trả về file từ query DB.*
- [ ] **Cảnh báo hành vi bất thường (đăng nhập nhiều lần sai, sửa dữ liệu hàng loạt)** - *Frontend: Form edit với dữ liệu cũ fill sẵn. Backend: Validate và update (PUT/PATCH) vào CSDL.*

### Cấu hình hệ thống
- [ ] **Cấu hình thông tin trường (tên, logo, địa chỉ, mã trường)**
- [ ] **Cấu hình SMTP gửi email**
- [ ] **Cấu hình gateway gửi SMS**
- [ ] **Cấu hình thời gian khóa/mở nhập điểm theo học kỳ** - *Backend: Khuyến nghị dùng Soft Delete (cập nhật cờ is_deleted/is_active) thay vì xóa cứng (DELETE) để bảo toàn khóa ngoại.*
- [ ] **Cấu hình tham số chung (năm học hiện hành, học kỳ hiện hành)**

### Sao lưu & Phục hồi
- [ ] **Sao lưu dữ liệu tự động theo lịch (hằng ngày/tuần)**
- [ ] **Sao lưu thủ công theo yêu cầu admin**
- [ ] **Phục hồi dữ liệu từ bản sao lưu**
- [ ] **Quản lý danh sách các bản sao lưu (xem, tải về, xóa)** - *Backend: Khuyến nghị dùng Soft Delete (cập nhật cờ is_deleted/is_active) thay vì xóa cứng (DELETE) để bảo toàn khóa ngoại.*
- [ ] **Thông báo kết quả sao lưu (thành công/thất bại)**

### Xác thực & Bảo mật
- [ ] **Đăng nhập bằng tài khoản/mật khẩu**
- [ ] **Xác thực OTP qua email/SMS (2FA)**
- [ ] **Khóa tài khoản tạm thời sau N lần đăng nhập sai** - *Backend: Khuyến nghị dùng Soft Delete (cập nhật cờ is_deleted/is_active) thay vì xóa cứng (DELETE) để bảo toàn khóa ngoại.*
- [ ] **Quản lý phiên đăng nhập (session) — cho phép đăng xuất từ xa** - *Backend: Sử dụng thư viện xuất file (vd: pandas, reportlab) để trả về file từ query DB.*
- [ ] **Chính sách mật khẩu (độ dài tối thiểu, ký tự đặc biệt, bắt buộc đổi định kỳ)**
- [ ] **Quản lý thiết bị đã đăng nhập**

### Hệ thống Thông báo nội bộ
- [ ] **Tạo và gửi thông báo thủ công (chọn người nhận theo vai trò/lớp/cá nhân)** - *Frontend: Form nhập liệu. Backend: Validate dữ liệu và insert (POST) vào CSDL.*
- [ ] **Tự động hóa thông báo theo sự kiện hệ thống (System Triggers)** - *Kỹ thuật: Dùng cơ chế Event/Signals trong framework backend để trigger hành động gửi mà không làm nghẽn luồng xử lý chính.*
- [ ] **Quản lý trạng thái thông báo (đã đọc/chưa đọc/đã xử lý)**
- [ ] **Phân loại thông báo và bộ lọc tìm kiếm** - *Backend: Xây dựng API hỗ trợ query params (GET), kết hợp phân trang (Pagination).*
- [ ] **Lịch sử thông báo đã gửi/nhận**

## MODULE 2: Quản lý danh mục gốc

### Danh mục đơn vị đào tạo
- [ ] **Thêm/sửa/xóa Khoa, Bộ môn, Trung tâm** - *Frontend: Form nhập liệu. Backend: Validate dữ liệu và insert (POST) vào CSDL.*
- [ ] **Quản lý cấu trúc phân cấp (Khoa → Bộ môn)**
- [ ] **Gán trưởng/phó đơn vị**
- [ ] **Trạng thái hoạt động/ngừng hoạt động của đơn vị**

### Danh mục ngành / chuyên ngành
- [ ] **Thêm/sửa/xóa ngành đào tạo** - *Frontend: Form nhập liệu. Backend: Validate dữ liệu và insert (POST) vào CSDL.*
- [ ] **Quản lý chuyên ngành trực thuộc ngành**
- [ ] **Quản lý hệ đào tạo (Chính quy, Liên thông, Vừa làm vừa học...)** - *Frontend: Form nhập liệu. Backend: Validate dữ liệu và insert (POST) vào CSDL.*
- [ ] **Gán ngành thuộc đơn vị (Khoa) quản lý**

### Danh mục khóa học & học kỳ
- [ ] **Quản lý khóa tuyển sinh (VD: Khóa 2024-2028)** - *Backend: Khuyến nghị dùng Soft Delete (cập nhật cờ is_deleted/is_active) thay vì xóa cứng (DELETE) để bảo toàn khóa ngoại.*
- [ ] **Quản lý năm học**
- [ ] **Quản lý học kỳ (HK1, HK2, Hè) gắn với năm học**
- [ ] **Thiết lập ngày bắt đầu/kết thúc học kỳ**

### Danh mục chương trình đào tạo
- [ ] **Xây dựng khung chương trình đào tạo theo ngành/khóa** - *Frontend: Form nhập liệu. Backend: Validate dữ liệu và insert (POST) vào CSDL.*
- [ ] **Thiết lập môn tiên quyết (prerequisite)** - *Logic: Phải join với bảng KQHT của học kỳ trước để xem sinh viên đã có điểm >= 5.0 (hoặc D) chưa.*
- [ ] **Thiết lập học phần thay thế/tương đương**
- [ ] **Quản lý số tín chỉ tối thiểu để tốt nghiệp**
- [ ] **Sao chép chương trình đào tạo từ khóa trước** - *Frontend: Form nhập liệu. Backend: Validate dữ liệu và insert (POST) vào CSDL.*

### Danh mục môn học / học phần
- [ ] **Thêm/sửa/xóa môn học (mã môn, tên môn)** - *Frontend: Form nhập liệu. Backend: Validate dữ liệu và insert (POST) vào CSDL.*
- [ ] **Thiết lập số tín chỉ (lý thuyết, thực hành)**
- [ ] **Phân loại học phần (bắt buộc, tự chọn, đại cương, chuyên ngành)**
- [ ] **Quản lý đề cương môn học (tài liệu đính kèm)**

### Danh mục phòng học
- [ ] **Thêm/sửa/xóa phòng học** - *Frontend: Form nhập liệu. Backend: Validate dữ liệu và insert (POST) vào CSDL.*
- [ ] **Phân loại phòng (lý thuyết, thực hành, hội trường)**
- [ ] **Thiết lập sức chứa từng phòng**
- [ ] **Trạng thái sử dụng (đang dùng, bảo trì)**

### Danh mục hình thức thi
- [ ] **Thêm/sửa các hình thức thi (viết, trắc nghiệm, vấn đáp, đồ án)** - *Frontend: Form nhập liệu. Backend: Validate dữ liệu và insert (POST) vào CSDL.*
- [ ] **Thiết lập thang điểm tương ứng từng hình thức**
- [ ] **Gán hình thức thi mặc định theo loại học phần**

### Danh mục đối tượng ưu tiên
- [ ] **Thêm/sửa danh mục đối tượng ưu tiên (khu vực, chính sách, dân tộc...)** - *Frontend: Form nhập liệu. Backend: Validate dữ liệu và insert (POST) vào CSDL.*
- [ ] **Thiết lập tỷ lệ/mức miễn giảm học phí tương ứng**
- [ ] **Thiết lập điểm cộng ưu tiên (nếu áp dụng xét tuyển/học bổng)**

### Danh mục khen thưởng / kỷ luật
- [ ] **Thêm/sửa các loại hình khen thưởng** - *Frontend: Form nhập liệu. Backend: Validate dữ liệu và insert (POST) vào CSDL.*
- [ ] **Thêm/sửa các loại hình kỷ luật** - *Frontend: Form nhập liệu. Backend: Validate dữ liệu và insert (POST) vào CSDL.*
- [ ] **Thiết lập điểm cộng/trừ rèn luyện tương ứng từng loại**
- [ ] **Thiết lập mức độ kỷ luật (khiển trách, cảnh cáo, đình chỉ, buộc thôi học)**

### Quản lý Sinh viên
- [ ] **Tạo hồ sơ sinh viên (thông tin cá nhân, liên hệ, gia đình)** - *Frontend: Form nhập liệu. Backend: Validate dữ liệu và insert (POST) vào CSDL.*

## MODULE 3: Quản lý nhân sự
- [ ] **Import danh sách sinh viên hàng loạt từ Excel** - *Backend: Sử dụng thư viện xuất file (vd: pandas, reportlab) để trả về file từ query DB.*
- [ ] **Cập nhật trạng thái học tập (đang học, bảo lưu, chuyển ngành, thôi học, tốt nghiệp)** - *Frontend: Form edit với dữ liệu cũ fill sẵn. Backend: Validate và update (PUT/PATCH) vào CSDL.*
- [ ] **Quản lý lịch sử lớp học theo từng học kỳ**
- [ ] **Tra cứu/tìm kiếm sinh viên theo nhiều tiêu chí** - *Backend: Xây dựng API hỗ trợ query params (GET), kết hợp phân trang (Pagination).*
- [ ] **Quản lý ảnh đại diện và giấy tờ đính kèm (CCCD, học bạ...)**
- [ ] **In thẻ sinh viên/giấy xác nhận**

### Quản lý Giảng viên
- [ ] **Tạo hồ sơ giảng viên (thông tin cá nhân, học vị, học hàm)** - *Frontend: Form nhập liệu. Backend: Validate dữ liệu và insert (POST) vào CSDL.*
- [ ] **Quản lý chuyên môn/lĩnh vực giảng dạy**
- [ ] **Quản lý lịch sử phân công giảng dạy**
- [ ] **Quản lý hợp đồng/biên chế (cơ hữu, thỉnh giảng)**
- [ ] **Tra cứu giảng viên theo khoa/bộ môn/chuyên môn** - *Backend: Xây dựng API hỗ trợ query params (GET), kết hợp phân trang (Pagination).*

### Quản lý Cán bộ - Nhân viên
- [ ] **Tạo hồ sơ nhân viên (giáo vụ, kế toán, thư viện, hành chính)** - *Frontend: Form nhập liệu. Backend: Validate dữ liệu và insert (POST) vào CSDL.*
- [ ] **Phân loại theo bộ phận/phòng ban**
- [ ] **Quản lý chức vụ, nhiệm vụ phụ trách**
- [ ] **Tra cứu/tìm kiếm nhân viên** - *Backend: Xây dựng API hỗ trợ query params (GET), kết hợp phân trang (Pagination).*

### Phân công giảng dạy
- [ ] **Gán giảng viên phụ trách cho từng lớp học phần**
- [ ] **Kiểm tra trùng lịch giảng dạy của giảng viên** - *Nghiệp vụ: So sánh Ca học + Ngày học + Phòng học/Giảng viên. Kỹ thuật: Query check Overlap Time trong SQL.*
- [ ] **Thống kê khối lượng giờ giảng theo giảng viên/học kỳ**
- [ ] **Điều chỉnh/thay đổi giảng viên phụ trách giữa kỳ**

### Kế hoạch đào tạo năm học
- [ ] **Lập kế hoạch mở môn học theo từng học kỳ/năm học**

## MODULE 4: Kế hoạch & Đăng ký học phần
- [ ] **Dự kiến số lớp, sĩ số mỗi môn** - *Database: Sử dụng Transaction và row-level locking (select_for_update) để chống xung đột (concurrency).*
- [ ] **Phê duyệt kế hoạch đào tạo (workflow duyệt)** - *Frontend: Form nhập liệu. Backend: Validate dữ liệu và insert (POST) vào CSDL.*
- [ ] **Sao chép kế hoạch từ học kỳ trước để điều chỉnh**

### Xây dựng thời khóa biểu
- [ ] **Xếp lịch học theo phòng/giảng viên/thời gian**
- [ ] **Kiểm tra trùng lịch (phòng, giảng viên, lớp)** - *Nghiệp vụ: So sánh Ca học + Ngày học + Phòng học/Giảng viên. Kỹ thuật: Query check Overlap Time trong SQL.*
- [ ] **Xếp lịch thi sơ bộ**
- [ ] **Xuất thời khóa biểu theo lớp/giảng viên/phòng** - *Backend: Khuyến nghị dùng Soft Delete (cập nhật cờ is_deleted/is_active) thay vì xóa cứng (DELETE) để bảo toàn khóa ngoại.*
- [ ] **Điều chỉnh thời khóa biểu khi có thay đổi** - *Backend: Khuyến nghị dùng Soft Delete (cập nhật cờ is_deleted/is_active) thay vì xóa cứng (DELETE) để bảo toàn khóa ngoại.*

### Mở lớp học phần
- [ ] **Tạo lớp học phần từ học phần trong chương trình đào tạo** - *Frontend: Form nhập liệu. Backend: Validate dữ liệu và insert (POST) vào CSDL.*
- [ ] **Thiết lập giới hạn sĩ số tối đa/tối thiểu** - *Database: Sử dụng Transaction và row-level locking (select_for_update) để chống xung đột (concurrency).*
- [ ] **Thiết lập điều kiện đăng ký (đã học môn tiên quyết...)** - *Logic: Phải join với bảng KQHT của học kỳ trước để xem sinh viên đã có điểm >= 5.0 (hoặc D) chưa.*
- [ ] **Đóng/hủy lớp học phần nếu không đủ sĩ số** - *Database: Sử dụng Transaction và row-level locking (select_for_update) để chống xung đột (concurrency).*

### Đăng ký học phần
- [ ] **Sinh viên xem danh sách lớp học phần mở trong kỳ**
- [ ] **Đăng ký học phần online**
- [ ] **Hệ thống tự kiểm tra điều kiện (môn tiên quyết, số tín chỉ tối đa)** - *Logic: Phải join với bảng KQHT của học kỳ trước để xem sinh viên đã có điểm >= 5.0 (hoặc D) chưa.*
- [ ] **Hệ thống tự kiểm tra xung đột lịch học** - *Nghiệp vụ: So sánh Ca học + Ngày học + Phòng học/Giảng viên. Kỹ thuật: Query check Overlap Time trong SQL.*
- [ ] **Xác nhận đăng ký thành công, xem phiếu đăng ký**

### Đăng ký ngoài kế hoạch
- [ ] **Đăng ký học lại (môn không đạt)**
- [ ] **Đăng ký học cải thiện điểm**
- [ ] **Đăng ký học vượt (vượt tiến độ)**
- [ ] **Phê duyệt các trường hợp đăng ký đặc biệt**

### Danh sách lớp chính thức
- [ ] **Chốt danh sách sinh viên sau thời gian đăng ký/điều chỉnh**
- [ ] **Đồng bộ danh sách sang module điểm danh**
- [ ] **Xuất danh sách lớp (file Excel/PDF) cho giảng viên** - *Backend: Sử dụng thư viện xuất file (vd: pandas, reportlab) để trả về file từ query DB.*
- [ ] **Khóa danh sách, không cho chỉnh sửa sau khi chốt** - *Frontend: Form edit với dữ liệu cũ fill sẵn. Backend: Validate và update (PUT/PATCH) vào CSDL.*

### Điều chỉnh đăng ký
- [ ] **Hủy đăng ký học phần trong thời gian quy định**
- [ ] **Đổi lớp học phần (chuyển từ lớp này sang lớp khác)**
- [ ] **Giới hạn thời gian được phép điều chỉnh**
- [ ] **Lưu lịch sử các lần điều chỉnh**

### Lập lịch thi
- [ ] **Xếp lịch thi theo môn/lớp học phần**

## MODULE 5: Khảo thí & Quản lý điểm
- [ ] **Xếp phòng thi, gán số lượng sinh viên/phòng**
- [ ] **Gán cán bộ coi thi (giám thị)**
- [ ] **Thiết lập hình thức thi cho từng kỳ thi**
- [ ] **Xuất lịch thi cho sinh viên/giảng viên** - *Backend: Sử dụng thư viện xuất file (vd: pandas, reportlab) để trả về file từ query DB.*

### Nhập điểm thành phần
- [ ] **Nhập điểm chuyên cần**
- [ ] **Nhập điểm giữa kỳ**
- [ ] **Nhập điểm thực hành/bài tập**
- [ ] **Thiết lập trọng số (%) từng thành phần**
- [ ] **Import điểm hàng loạt từ Excel** - *Backend: Sử dụng thư viện xuất file (vd: pandas, reportlab) để trả về file từ query DB.*

### Nhập điểm cuối kỳ
- [ ] **Nhập điểm thi cuối kỳ**
- [ ] **Khóa điểm sau thời hạn quy định (không cho sửa)** - *Frontend: Form edit với dữ liệu cũ fill sẵn. Backend: Validate và update (PUT/PATCH) vào CSDL.*
- [ ] **Giảng viên gửi yêu cầu mở khóa điểm khi cần chỉnh sửa** - *Frontend: Form edit với dữ liệu cũ fill sẵn. Backend: Validate và update (PUT/PATCH) vào CSDL.*
- [ ] **Lịch sử thay đổi điểm (ai sửa, khi nào)** - *Frontend: Form edit với dữ liệu cũ fill sẵn. Backend: Validate và update (PUT/PATCH) vào CSDL.*

### Tính điểm tổng kết
- [ ] **Tự động tính điểm tổng kết học phần theo trọng số**
- [ ] **Quy đổi điểm hệ 10 sang hệ 4 và điểm chữ (A, B, C...)** - *Nghiệp vụ: Áp dụng công thức (Tổng điểm * Số tín chỉ)/Tổng tín chỉ. Cần chạy background task hoặc tính lại mỗi khi điểm thay đổi.*
- [ ] **Tính điểm trung bình học kỳ (GPA kỳ)**
- [ ] **Tính điểm trung bình tích lũy (CPA)**
- [ ] **Xếp loại học lực theo điểm trung bình**

### Phúc khảo
- [ ] **Sinh viên gửi đơn phúc khảo online**
- [ ] **Giáo vụ tiếp nhận, phân công chấm phúc khảo**
- [ ] **Cập nhật kết quả phúc khảo (giữ nguyên/thay đổi điểm)** - *Frontend: Form edit với dữ liệu cũ fill sẵn. Backend: Validate và update (PUT/PATCH) vào CSDL.*
- [ ] **Thông báo kết quả phúc khảo cho sinh viên**

### Bảng điểm
- [ ] **Tra cứu điểm theo từng học kỳ** - *Backend: Xây dựng API hỗ trợ query params (GET), kết hợp phân trang (Pagination).*
- [ ] **Tra cứu điểm tích lũy toàn khóa** - *Backend: Khuyến nghị dùng Soft Delete (cập nhật cờ is_deleted/is_active) thay vì xóa cứng (DELETE) để bảo toàn khóa ngoại.*
- [ ] **Xuất bảng điểm (PDF) có xác nhận của trường** - *Backend: Sử dụng thư viện xuất file (vd: pandas, reportlab) để trả về file từ query DB.*
- [ ] **In bảng điểm tạm thời/chính thức**

### Cảnh báo học vụ
- [ ] **Tự động phát hiện sinh viên có GPA dưới ngưỡng**
- [ ] **Phát hiện sinh viên nợ môn vượt mức quy định**
- [ ] **Gửi thông báo cảnh báo học vụ tới sinh viên/cố vấn**
- [ ] **Theo dõi danh sách sinh viên bị cảnh báo qua các kỳ**

### Điểm rèn luyện
- [ ] **Sinh viên tự đánh giá điểm rèn luyện (nếu áp dụng)**

## MODULE 6: Công tác sinh viên & Rèn luyện
- [ ] **Lớp/cố vấn xét duyệt điểm rèn luyện**
- [ ] **Tính điểm và xếp loại rèn luyện theo kỳ**
- [ ] **Tra cứu lịch sử điểm rèn luyện qua các kỳ** - *Backend: Xây dựng API hỗ trợ query params (GET), kết hợp phân trang (Pagination).*

### Khen thưởng - Kỷ luật
- [ ] **Lập và quản lý quyết định khen thưởng (theo danh mục)**
- [ ] **Lập và quản lý quyết định kỷ luật**
- [ ] **Đính kèm văn bản quyết định**
- [ ] **Tra cứu lịch sử khen thưởng/kỷ luật theo sinh viên** - *Backend: Xây dựng API hỗ trợ query params (GET), kết hợp phân trang (Pagination).*

### Học bổng
- [ ] **Thiết lập tiêu chí xét học bổng (theo GPA, rèn luyện, hoàn cảnh)**
- [ ] **Lập danh sách sinh viên đủ điều kiện xét**
- [ ] **Phê duyệt danh sách nhận học bổng**
- [ ] **Thông báo kết quả học bổng**

### Cố vấn học tập
- [ ] **Phân công cố vấn học tập cho từng lớp/sinh viên**
- [ ] **Ghi nhận nội dung tư vấn, buổi gặp**
- [ ] **Cố vấn xem được tình hình học tập của sinh viên phụ trách**
- [ ] **Lịch sử các lần tư vấn**

### Khảo sát sinh viên
- [ ] **Tạo phiếu khảo sát (đánh giá môn học, giảng viên)** - *Frontend: Form nhập liệu. Backend: Validate dữ liệu và insert (POST) vào CSDL.*
- [ ] **Sinh viên thực hiện khảo sát online**
- [ ] **Tổng hợp kết quả khảo sát theo môn/giảng viên**
- [ ] **Xuất báo cáo khảo sát** - *Backend: Sử dụng thư viện xuất file (vd: pandas, reportlab) để trả về file từ query DB.*

### Bảo hiểm y tế
- [ ] **Quản lý danh sách sinh viên tham gia BHYT**
- [ ] **Theo dõi thời hạn tham gia/hết hạn**
- [ ] **Ghi nhận thanh toán phí BHYT**
- [ ] **Xuất danh sách báo cáo BHYT theo lớp/khóa** - *Backend: Khuyến nghị dùng Soft Delete (cập nhật cờ is_deleted/is_active) thay vì xóa cứng (DELETE) để bảo toàn khóa ngoại.*

### Thiết lập học phí
- [ ] **Cấu hình đơn giá học phí theo tín chỉ**

## MODULE 7: Tài chính & Học phí
- [ ] **Thiết lập mức học phí riêng theo ngành/hệ đào tạo (nếu khác nhau)** - *Frontend: Form nhập liệu. Backend: Validate dữ liệu và insert (POST) vào CSDL.*
- [ ] **Cập nhật đơn giá theo từng năm học** - *Frontend: Form edit với dữ liệu cũ fill sẵn. Backend: Validate và update (PUT/PATCH) vào CSDL.*

### Tính công nợ
- [ ] **Tự động sinh công nợ học phí dựa trên đăng ký học phần** - *Nghiệp vụ: Tự động chốt công nợ vào đầu kỳ. Kỹ thuật: Cần có liên kết (ForeignKey) chuẩn xác tới bảng Đăng ký học phần để đếm số tín chỉ.*
- [ ] **Theo dõi tình trạng công nợ (đã đóng, còn nợ, quá hạn)**
- [ ] **Gửi thông báo nhắc nợ tự động** - *Kỹ thuật: Dùng cơ chế Event/Signals trong framework backend để trigger hành động gửi mà không làm nghẽn luồng xử lý chính.*
- [ ] **Tự động hoàn trả học phí/công nợ cho sinh viên khi lớp học phần bị hủy**
- [ ] **Tổng hợp công nợ theo lớp/khóa/sinh viên** - *Backend: Khuyến nghị dùng Soft Delete (cập nhật cờ is_deleted/is_active) thay vì xóa cứng (DELETE) để bảo toàn khóa ngoại.*

### Quản lý phiếu thu
- [ ] **Lập phiếu thu học phí**
- [ ] **In biên lai thu tiền**
- [ ] **Ghi nhận hình thức thanh toán (tiền mặt, chuyển khoản, online)**
- [ ] **Tra cứu lịch sử thanh toán theo sinh viên** - *Backend: Xây dựng API hỗ trợ query params (GET), kết hợp phân trang (Pagination).*

### Miễn giảm & Gia hạn
- [ ] **Lập hồ sơ xét miễn giảm học phí (theo đối tượng ưu tiên)**
- [ ] **Phê duyệt miễn giảm**
- [ ] **Gia hạn thời gian đóng học phí**
- [ ] **Theo dõi danh sách sinh viên được miễn giảm/gia hạn**

### Tài khoản ngân hàng
- [ ] **Kết nối cổng thanh toán trực tuyến (VNPay, Momo, ngân hàng...)**
- [ ] **Đối soát giao dịch thanh toán tự động** - *Database: Sử dụng Transaction và row-level locking (select_for_update) để chống xung đột (concurrency).*
- [ ] **Xử lý giao dịch lỗi/hoàn tiền** - *Database: Sử dụng Transaction và row-level locking (select_for_update) để chống xung đột (concurrency).*
- [ ] **Lịch sử giao dịch qua cổng thanh toán** - *Database: Sử dụng Transaction và row-level locking (select_for_update) để chống xung đột (concurrency).*

### Quản lý hoàn trả / Giảm trừ
- [ ] **Tự động hoàn trả/giảm trừ công nợ khi lớp học phần bị hủy.** - *Logic sẽ kích hoạt (Trigger) ngay khi trạng thái lớp ở Module 4 chuyển thành "Hủy". Hệ thống bắt buộc phải sử dụng Transaction trong Database để đảm bảo tiền/tín chỉ được hoàn về tài khoản sinh viên đồng bộ với việc xóa tên khỏi danh sách lớp, tránh thất thoát dữ liệu.*

## MODULE 8: Thẩm định & Xét tốt nghiệp

### Điều kiện tốt nghiệp
- [ ] **Thiết lập điều kiện tốt nghiệp theo ngành (tín chỉ, GPA, chứng chỉ, rèn luyện...)**
- [ ] **Cấu hình điều kiện theo từng khóa (có thể khác nhau)** - *Backend: Khuyến nghị dùng Soft Delete (cập nhật cờ is_deleted/is_active) thay vì xóa cứng (DELETE) để bảo toàn khóa ngoại.*

### Kiểm tra điều kiện
- [ ] **Đối chiếu tự động điều kiện tốt nghiệp với hồ sơ từng sinh viên**
- [ ] **Hiển thị danh sách điều kiện còn thiếu (nếu có)**
- [ ] **Sinh viên tự tra cứu tiến độ đủ điều kiện tốt nghiệp** - *Backend: Xây dựng API hỗ trợ query params (GET), kết hợp phân trang (Pagination).*

### Danh sách xét tốt nghiệp
- [ ] **Lập danh sách sinh viên đủ điều kiện theo đợt xét**
- [ ] **Trình hội đồng phê duyệt danh sách**
- [ ] **Công bố danh sách chính thức được công nhận tốt nghiệp**

### Quản lý phôi bằng
- [ ] **Quản lý số lượng phôi bằng tồn/đã sử dụng**
- [ ] **In bằng tốt nghiệp**
- [ ] **In bảng điểm toàn khóa kèm theo bằng** - *Backend: Khuyến nghị dùng Soft Delete (cập nhật cờ is_deleted/is_active) thay vì xóa cứng (DELETE) để bảo toàn khóa ngoại.*
- [ ] **Quản lý số hiệu, số vào sổ cấp bằng**

### Hồ sơ tốt nghiệp
- [ ] **Theo dõi tình trạng nhận bằng của từng sinh viên**
- [ ] **Ghi nhận ngày nhận bằng, người nhận thay (nếu có ủy quyền)**
- [ ] **Lưu trữ hồ sơ tốt nghiệp điện tử**

### Xét tốt nghiệp sớm / muộn
- [ ] **Xử lý trường hợp sinh viên chuyển trường**
- [ ] **Xử lý trường hợp chương trình đào tạo thay đổi giữa khóa học** - *Frontend: Form nhập liệu. Backend: Validate dữ liệu và insert (POST) vào CSDL.*
- [ ] **Xử lý trường hợp sinh viên bị kỷ luật/đình chỉ ảnh hưởng tốt nghiệp**
- [ ] **Xét đặc cách/đặc biệt theo quy định riêng**

### Quản lý Đồ án & Thẩm định Tốt nghiệp
- [ ] **Đăng ký đề tài đồ án/khóa luận tốt nghiệp** - *Backend: Khuyến nghị dùng Soft Delete (cập nhật cờ is_deleted/is_active) thay vì xóa cứng (DELETE) để bảo toàn khóa ngoại.*
- [ ] **Phân công giảng viên hướng dẫn**
- [ ] **Phân công giảng viên phản biện**
- [ ] **Thành lập hội đồng bảo vệ (thành viên, chủ tịch, thư ký)**
- [ ] **Lên lịch bảo vệ**
- [ ] **Chấm điểm khóa luận/đồ án (điểm hướng dẫn, phản biện, hội đồng)** - *Backend: Khuyến nghị dùng Soft Delete (cập nhật cờ is_deleted/is_active) thay vì xóa cứng (DELETE) để bảo toàn khóa ngoại.*
- [ ] **Tổng hợp kết quả bảo vệ**

### Chuyển đổi tín chỉ & Học phần tương đương
- [ ] **Thiết lập bộ quy tắc môn học tương đương (Mapping Rules) giữa các ngành.**
- [ ] **Ánh xạ (Map) kết quả học tập từ khung chương trình cũ sang khung mới. Clone bản ghi điểm để bảo toàn lịch sử thay vì sửa trực tiếp.**
- [ ] **Tự động loại bỏ các môn không tương đương (chuyển thành môn ngoài khung), tách chúng khỏi thuật toán tính GPA của ngành mới.**

## MODULE 9: Thống kê & Báo cáo

### Dashboard
- [ ] **Biểu đồ tổng quan số lượng sinh viên (theo khóa/ngành/trạng thái)** - *Backend: Khuyến nghị dùng Soft Delete (cập nhật cờ is_deleted/is_active) thay vì xóa cứng (DELETE) để bảo toàn khóa ngoại.*
- [ ] **Biểu đồ tổng quan tình hình học phí (đã thu/còn nợ)**
- [ ] **Biểu đồ tổng quan đào tạo (số lớp, số môn mở trong kỳ)** - *Frontend: Form nhập liệu. Backend: Validate dữ liệu và insert (POST) vào CSDL.*
- [ ] **Tùy chỉnh widget hiển thị theo vai trò người dùng**

### Báo cáo đào tạo
- [ ] **Thống kê số lượng sinh viên theo khoa/ngành/khóa** - *Backend: Khuyến nghị dùng Soft Delete (cập nhật cờ is_deleted/is_active) thay vì xóa cứng (DELETE) để bảo toàn khóa ngoại.*
- [ ] **Thống kê số lớp học phần mở theo học kỳ**
- [ ] **Xuất báo cáo theo nhiều định dạng** - *Backend: Sử dụng thư viện xuất file (vd: pandas, reportlab) để trả về file từ query DB.*

### Báo cáo học tập
- [ ] **Thống kê học lực sinh viên (giỏi, khá, trung bình, yếu)**
- [ ] **Thống kê tỷ lệ đạt/trượt theo môn học**
- [ ] **Thống kê theo lớp/khóa/ngành** - *Backend: Khuyến nghị dùng Soft Delete (cập nhật cờ is_deleted/is_active) thay vì xóa cứng (DELETE) để bảo toàn khóa ngoại.*

### Báo cáo tài chính
- [ ] **Tổng hợp số liệu thu học phí theo kỳ/năm**
- [ ] **Tổng hợp công nợ còn tồn đọng**
- [ ] **Báo cáo doanh thu theo khoa/ngành**

### Báo cáo nhân sự
- [ ] **Thống kê số lượng giảng viên theo khoa/bộ môn**
- [ ] **Thống kê giờ giảng theo giảng viên/học kỳ**
- [ ] **Báo cáo khối lượng công tác**

### Báo cáo khảo thí
- [ ] **Thống kê lịch thi đã tổ chức**
- [ ] **Thống kê kết quả thi theo môn/lớp**
- [ ] **Báo cáo tỷ lệ phúc khảo và kết quả phúc khảo**

### Báo cáo tùy chỉnh
- [ ] **Cho phép người dùng tự chọn tiêu chí, cột dữ liệu để xuất báo cáo** - *Backend: Sử dụng thư viện xuất file (vd: pandas, reportlab) để trả về file từ query DB.*
- [ ] **Xuất báo cáo ra Excel** - *Backend: Sử dụng thư viện xuất file (vd: pandas, reportlab) để trả về file từ query DB.*
- [ ] **Xuất báo cáo ra PDF** - *Backend: Sử dụng thư viện xuất file (vd: pandas, reportlab) để trả về file từ query DB.*
- [ ] **Lưu mẫu báo cáo đã tùy chỉnh để dùng lại**

### Xuất dữ liệu
- [ ] **Xuất dữ liệu sinh viên/điểm/tốt nghiệp theo mẫu chuẩn của Bộ GD&ĐT** - *Backend: Sử dụng thư viện xuất file (vd: pandas, reportlab) để trả về file từ query DB.*
- [ ] **Kiểm tra tính hợp lệ dữ liệu trước khi xuất** - *Backend: Sử dụng thư viện xuất file (vd: pandas, reportlab) để trả về file từ query DB.*
- [ ] **Lưu lịch sử các lần xuất dữ liệu** - *Backend: Sử dụng thư viện xuất file (vd: pandas, reportlab) để trả về file từ query DB.*