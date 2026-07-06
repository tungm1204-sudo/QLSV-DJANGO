# KẾ HOẠCH LÀM VIỆC NHÓM (2 DEVELOPERS)

Tài liệu này định nghĩa cách 2 lập trình viên sẽ phối hợp với nhau để phát triển hệ thống SIS một cách trơn tru, tránh dẫm chân lên nhau và kiểm soát chất lượng code.

---

## 1. CHIẾN LƯỢC PHÂN CHIA NHIỆM VỤ (THEO MODULE)

Dựa trên nguyên tắc cấu trúc **Feature-based**, chúng ta sẽ chọn **Phương án chia theo Dọc (Fullstack)**. Mỗi người sẽ làm từ A-Z (cả DB, API và giao diện React) cho Module được giao. 

### Lộ trình Code (Sprint Plan) - Phân giải phụ thuộc

Vì các module có tính phụ thuộc dữ liệu lẫn nhau, 2 bạn **không thể làm song song hoàn toàn ngay từ đầu** mà phải chia làm 3 giai đoạn:

#### Giai đoạn 1: Xây móng (Bắt buộc tuần tự / Làm cùng nhau)
Ở tuần đầu tiên, phải làm xong các module gốc (không phụ thuộc bảng khác).
- **Dev A:** Làm module **`identity`** (Account, Role, Phân quyền).
- **Dev B:** Làm module **`master_data`** (Khoa, Ngành học, Phòng học, Năm học).
👉 *Hoàn thành xong phải Review chéo và Merge ngay vào nhánh `develop`.*

#### Giai đoạn 2: Lắp khung (Phụ thuộc Giai đoạn 1)
- **Dev A:** Làm module **`hr`** (Hồ sơ Sinh viên, Giảng viên). Cần dùng `Account` và `Khoa/Ngành` từ Giai đoạn 1.
- **Dev B:** Làm module **`curriculum`** (Môn học, Chương trình đào tạo, Lớp học phần).
👉 *Merge tiếp vào `develop` để có data gốc (Sinh viên, Môn học) cho các chức năng sau.*

#### Giai đoạn 3: Phân nhánh độc lập (Song song 100%)
Lúc này đã có đủ data nền tảng, 2 bạn có thể chia nhau làm hoàn toàn độc lập:
- **Dev A:** Nhận thầu **`affairs`** (Khen thưởng, Kỷ luật, Điểm rèn luyện) và **`dashboard`**.
- **Dev B:** Nhận thầu **`enrollment`** (Đăng ký học phần, xếp TKB), **`finance`** (Học phí, Hóa đơn) và **`exams`** (Nhập điểm, Khảo thí).

---

## 2. QUY TẮC GIAO TIẾP VÀ ĐỒNG BỘ 

Với team 2 người, giao tiếp nhanh gọn là ưu tiên hàng đầu.

### A. Học/Sync-up hàng ngày (Daily Stand-up)
- **Công cụ:** Discord, Zalo, hoặc Google Meet.
- **Thời gian:** Dành ra 10-15 phút mỗi sáng hoặc tối trước khi bắt đầu code.
- **Nội dung:** Trả lời 3 câu hỏi:
  1. Hôm qua đã làm xong gì? (VD: Đã push xong API Đăng nhập).
  2. Hôm nay dự định làm gì?
  3. Có đang bị kẹt (block) chỗ nào không? Cần người kia support gì không?

### B. Quản lý Tiến độ (Ticket)
- Lấy Sơ đồ Use Case (`system_diagrams.md`) đẻ ra các Ticket trên **Trello** hoặc **GitHub Projects**.
- Bảng Kanban gồm 4 cột: `To Do` -> `In Progress` -> `In Review` -> `Done`.
- Ai làm tính năng nào phải tự kéo Ticket của mình sang `In Progress`.

### C. Giao tiếp qua Code (Review Chéo)
- **Git Flow:** Tạo nhánh từ `develop` (VD: `feature/auth-login`). Tuyệt đối không commit trực tiếp vào `main`/`develop`.
- **Review Chéo (BẮT BUỘC):** Khi Dev A làm xong, đẩy Pull Request (PR). Thay vì chat "Ê m duyệt code cho tớ đi", Dev A phải mô tả rõ trong PR: *"Tớ vừa làm hàm check trùng email, cậu xem ổn không"*.
- Dev B bắt buộc phải vào đọc code. Nếu thấy vi phạm `rules.md` (chưa xử lý N+1, logic viết nhầm vào View), Dev B được quyền **Request Changes** và bôi đỏ ngay dòng code đó để Dev A sửa. Đạt chuẩn mới bấm **Approve**.

### D. Đồng bộ API Contract
- Khi một người viết xong 1 API (Backend), không cần chụp màn hình gửi qua chat. 
- Thay vào đó, truy cập thẳng vào trang **Swagger UI** (do hệ thống sinh tự động qua `drf-spectacular`) hoặc đưa vào chung 1 workspace trên **Postman**. Người kia chỉ việc mở ra là biết cần truyền body gì, response trả về ra sao.

---

## 3. VAI TRÒ CỦA REPO GITHUB & RULES.MD

Tài liệu `rules.md` hiện tại đóng vai trò là "Trọng tài" (Source of Truth). 
- Khi 2 người có bất đồng quan điểm về phong cách code, cứ mở `rules.md` ra làm chuẩn mực. Không cãi cọ cá nhân.
- Nếu trong lúc làm việc phát sinh một chuẩn mực mới, cả 2 phải thống nhất cập nhật vào `rules.md` rồi commit lên git để làm luật chung. 
- Mọi tài liệu (như file này, hay sơ đồ diagram) luôn đi kèm code trong repo để bất cứ ai (dù là người mới vào team) khi clone code về cũng hiểu rõ ngay cách vận hành.
