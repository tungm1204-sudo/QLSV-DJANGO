Dựa trên yêu cầu **không làm song song** và **chia nhỏ khối lượng công việc để hoàn thành trong 2-3 ngày/đợt**, chúng ta sẽ áp dụng chiến lược **Backend đi trước, Frontend theo sau (Strict Sequential Handoff)**.

Toàn bộ hệ thống SIS (với đầy đủ 100% tính năng trong `FEATURE_CHECKLIST.md`) được chia thành **5 Khối (Blocks)**. Mỗi khối kéo dài đúng 3 ngày:
*   **Ngày 1 & 2:** Dev A phụ trách toàn bộ Backend API (chia làm 2 phần nhỏ).
*   **Ngày 3:** Dev B kéo code của Dev A về để ráp giao diện (UI/UX) cho phần API đó.

Như vậy, khối lượng được chia đều, 2 Dev không bao giờ sửa chung file cùng lúc, hạn chế tuyệt đối Conflict và lỗi Quota.

---

### Lộ trình 3 Tuần (15 Ngày Làm Việc) - Strict Turn-based Handoff

#### 📅 KHỐI 1 (Ngày 1-3): HỆ THỐNG & BẢO MẬT (Module 1)
*   **Ngày 1 (Dev A - Backend P1):** Tạo DB, cấu hình Django. Lập Model `User` (chưa có Role), API Đăng nhập (JWT), API Quản lý Người dùng (CRUD, Reset mật khẩu, Import Excel, Lịch sử đăng nhập).
*   **Ngày 2 (Dev A - Backend P2):** API Phân quyền (`Role`, Ma trận quyền, Gán quyền menu), Nhật ký hệ thống (Audit Log, xuất PDF/Excel), Cấu hình hệ thống (SMTP, SMS, Tham số chung), Xác thực (OTP, Khóa tài khoản do nhập sai, Quản lý phiên), Hệ thống Thông báo nội bộ (Tự động gửi/Thủ công).
*   **Ngày 3 (Dev B - Frontend):** Kéo code Dev A. Cài React, Tailwind, Zustand. Dựng Base Layout (Sidebar, Header, Auth Guard). Ghép giao diện toàn bộ module Identity (Login, Quản lý tài khoản, Phân quyền, Log, Cấu hình, Thông báo). Merge vào `develop`.

#### 📅 KHỐI 2 (Ngày 4-6): DANH MỤC GỐC & NHÂN SỰ (Module 2, 3)
*   **Ngày 4 (Dev A - Backend P1 - Master Data):** API Đơn vị đào tạo (Khoa/Bộ môn), Ngành/Chuyên ngành, Khóa học/Học kỳ, Chương trình đào tạo (Khung, môn tiên quyết, số tín chỉ), Môn học/Học phần, Phòng học, Hình thức thi, Đối tượng ưu tiên, Khen thưởng/Kỷ luật.
*   **Ngày 5 (Dev A - Backend P2 - HR):** API Quản lý Sinh viên (Hồ sơ, Import Excel, Trạng thái), Giảng viên, Cán bộ/Nhân viên, Phân công giảng dạy (Gán GV cho lớp, Kiểm tra trùng lịch dạy).
*   **Ngày 6 (Dev B - Frontend):** Kéo code. Ráp giao diện (UI) cho toàn bộ màn hình Quản lý Danh mục gốc và Hồ sơ Sinh viên, Giảng viên, Cán bộ. Merge vào `develop`.

#### 📅 KHỐI 3 (Ngày 7-9): ĐÀO TẠO & ĐĂNG KÝ HỌC PHẦN (Module 4)
*   **Ngày 7 (Dev A - Backend P1 - Curriculum):** API Kế hoạch đào tạo năm học (Sao chép, Phê duyệt), Xây dựng Thời khóa biểu (Xếp lịch, Kiểm tra trùng lịch phòng/GV), Mở lớp học phần (Điều kiện đăng ký, Giới hạn sĩ số).
*   **Ngày 8 (Dev A - Backend P2 - Enrollment):** API Đăng ký học phần (Kiểm tra điều kiện tiên quyết, Kiểm tra xung đột lịch), Đăng ký ngoài kế hoạch (Học cải thiện, Học vượt), Chốt danh sách lớp, Điều chỉnh đăng ký (Đổi lớp, Hủy lớp) sử dụng Database Transaction để chống Race Condition.
*   **Ngày 9 (Dev B - Frontend):** Kéo code. Ráp màn hình Lên kế hoạch đào tạo cho Giáo vụ và màn hình Đăng ký tín chỉ online cực kỳ quan trọng cho Sinh viên.

#### 📅 KHỐI 4 (Ngày 10-12): KHẢO THÍ, RÈN LUYỆN & TÀI CHÍNH (Module 5, 6, 7)
*   **Ngày 10 (Dev A - Backend P1 - Exams & Affairs):** API Lập lịch thi, Nhập điểm (thành phần, cuối kỳ, khóa điểm), Tính điểm tổng kết (GPA, CPA, hệ 4, chữ), Phúc khảo, Cảnh báo học vụ. API Điểm rèn luyện, Kỷ luật/Khen thưởng, Học bổng, Cố vấn học tập, Khảo sát sinh viên, Bảo hiểm y tế.
*   **Ngày 11 (Dev A - Backend P2 - Finance):** API Thiết lập học phí (Đơn giá), Tính công nợ tự động dựa trên tín chỉ, Quản lý phiếu thu, Miễn giảm/Gia hạn, Kết nối tài khoản ngân hàng, Quản lý hoàn trả/giảm trừ tự động khi hủy lớp.
*   **Ngày 12 (Dev B - Frontend):** Kéo code. Ráp giao diện Nhập điểm, Phúc khảo, Rèn luyện, Cố vấn học tập và Thanh toán công nợ học phí.

#### 📅 KHỐI 5 (Ngày 13-15): TỐT NGHIỆP, THỐNG KÊ & BÀN GIAO (Module 8, 9)
*   **Ngày 13 (Dev A - Backend P1 - Graduation):** API Thiết lập điều kiện tốt nghiệp, Tự động đối chiếu điều kiện, Danh sách xét tốt nghiệp, Quản lý phôi bằng. API Đồ án (Đăng ký đề tài, Hướng dẫn, Phản biện, Chấm điểm), Chuyển đổi tín chỉ/Học phần tương đương.
*   **Ngày 14 (Dev A - Backend P2 - Reports):** Dashboard biểu đồ tổng quan, Thống kê Đào tạo/Học tập/Tài chính/Nhân sự/Khảo thí. API Xuất báo cáo tùy chỉnh, Xuất dữ liệu chuẩn Bộ GD&ĐT (Excel/PDF). API Sao lưu & Phục hồi dữ liệu hệ thống.
*   **Ngày 15 (Dev B - Frontend & QC):** Kéo code. Ráp giao diện Xét tốt nghiệp, Đồ án, Biểu đồ Dashboard và Báo cáo. Cả 2 Dev test toàn hệ thống, tối ưu DB, fix bugs. Merge `main` và Deploy.

---

## 2. QUY TẮC GIAO TIẾP VÀ ĐỒNG BỘ 

Với team 2 người làm tuần tự, giao tiếp cực kỳ quan trọng ở các điểm chuyển giao (Handoff).

### A. Quy trình Chuyển giao (Handoff)
- **Ngày 1-2 (Dev A làm):** Khi xong từng API, Dev A phải cập nhật ngay vào Swagger/Postman để Dev B nghiên cứu trước. 
- **Ngày 3 (Dev B làm):** Dev B kéo code từ nhánh của Dev A và trực tiếp ráp React. Dev B sẽ báo Dev A nếu API thiếu trường (Field) để Dev A sửa nhanh.
- **Cuối Ngày 3:** Test chéo toàn bộ Khối đó và Merge vào `develop`.

### B. Quản lý Tiến độ (Ticket)
- Dựa vào lịch trình 5 Khối ở trên để vạch ra Ticket trên Trello. Mỗi Khối tạo chính xác 3 Ticket (Tương ứng Ngày 1, Ngày 2, Ngày 3).

### C. Vai trò của Repo & Rules.md
Tài liệu `rules.md` hiện tại đóng vai trò là "Trọng tài". Mọi vấn đề về code style, format API Response, hay cách đặt tên biến đều phải chiếu theo `rules.md`. Khuyến khích tham chiếu `FEATURE_CHECKLIST.md` để đảm bảo không rớt tính năng.
