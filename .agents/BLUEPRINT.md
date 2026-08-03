# 🧭 BLUEPRINT CHO AI AGENT VÀ TEAM PHÁT TRIỂN

Tài liệu này đóng vai trò blueprint vận hành cho dự án QLSV-DJANGO và có thể tái sử dụng cho các dự án khác.

---

## 1. MỤC TIÊU

Blueprint này nhằm giúp AI agent và developer làm việc đúng theo 4 nguyên tắc:

1. Đọc tài liệu trước khi code
2. Tuân thủ kiến trúc đã định sẵn
3. Kiểm tra yêu cầu bằng checklist trước khi triển khai
4. Verify thật kỹ trước khi báo cáo hoàn thành

---

## 2. NGUYÊN TẮC CỐT LÕI

### 2.1 Docs-first
Trước khi sửa code hoặc thêm feature, agent phải đọc ít nhất:

- docs/architecture/rules.md
- docs/architecture/system_diagrams.md
- docs/management/FEATURE_CHECKLIST.md
- docs/management/TEAM_WORKFLOW.md
- docs/CHANGELOG.md
- docs/database.dbml

Nếu thiếu thông tin, agent phải dừng lại và hỏi user thay vì đoán.

### 2.2 Architecture-first
Không được phá cấu trúc đã thống nhất.

- View: mỏng, chỉ nhận request và gọi service
- Service: chứa logic nghiệp vụ
- Selector: chứa query phức tạp
- Serializer: validate và format, không chứa business logic
- Transaction: dùng khi thao tác nhiều bảng
- Permission: phải kiểm tra thật chặt

### 2.3 Checklist-first
Mọi feature phải được đối chiếu với FEATURE_CHECKLIST trước khi triển khai.

Nếu task là feature mới, phải chắc chắn đã tồn tại trong checklist. Nếu chưa, cần ghi nhận và xác nhận với user.

### 2.4 Test-first for bug fix
Đối với bug, agent phải:

- xác định nguyên nhân
- tạo case kiểm thử hoặc mô tả case trước khi sửa
- sửa tối thiểu
- verify bằng test hoặc chạy thực tế

---

## 3. QUY TRÌNH LÀM VIỆC CHO AGENT

### Bước 1: Thu thập ngữ cảnh
Agent phải đọc:

- yêu cầu user
- docs liên quan
- code hiện tại
- model / serializer / view / service liên quan

### Bước 2: Lập kế hoạch
Trước khi code, agent phải viết một implementation plan ngắn gồm:

- mục tiêu
- file sẽ chỉnh sửa
- logic chính
- rủi ro / edge case
- test cần chạy

### Bước 3: Thực thi
Agent phải code đúng tầng và đúng nguyên tắc:

- không viết logic nghiệp vụ trong view/serializer
- không dùng query thô không cần thiết
- không hardcode secret/token/password
- không bỏ qua permission

### Bước 4: Verify
Sau khi code, agent phải:

- chạy test / check
- kiểm tra lỗi syntax
- kiểm tra API response
- nếu có frontend thì test UI thực tế
- nếu có thay đổi API/schema thì cập nhật changelog

---

## 4. QUY TẮC REVIEW CHO MỖI TASK

### 4.1 Review theo 5 lớp
Mỗi task nên được review theo 5 lớp:

1. Yêu cầu: đúng checklist chưa?
2. Kiến trúc: đúng tầng chưa?
3. Bảo mật: có lộ quyền/secret không?
4. Dữ liệu: có đúng model/status/field không?
5. Test: có verify chưa?

### 4.2 Câu hỏi bắt buộc trước khi làm
Agent phải tự hỏi trước khi sửa hoặc viết code:

- Đây là requirement gì?
- Contract hiện tại có ghi rõ không?
- Model/status/field có đúng không?
- Ai được phép làm hành động này?
- Nếu sai thì hệ thống sẽ phản hồi thế nào?
- Có test nào cần có không?

---

## 5. QUY TẮC BẢO MẬT

Agent phải luôn tuân thủ:

- không hardcode secret key/password/token
- không trả dữ liệu nhạy cảm trong response
- kiểm tra permission trước khi thao tác
- không cho phép client tự bypass logic nghiệp vụ nếu không có quyền
- không lưu mật khẩu plaintext trong file export/import

---

## 6. QUY TẮC CHO TEAM THỰC TẾ

### 6.1 Phân chia công việc
Theo workflow của dự án, team nên làm tuần tự:

- Backend trước
- Frontend sau
- Review và test chéo ở cuối mỗi block

### 6.2 Handoff checklist
Mỗi khi chuyển giao giữa backend và frontend, cần có:

- API đã có swagger/docs
- response shape rõ ràng
- field cần dùng đã có sẵn
- lỗi logic cần ghi chú
- test case đã chạy

### 6.3 Tài liệu cập nhật
Mọi thay đổi quan trọng cần ghi vào:

- CHANGELOG.md
- database.dbml (nếu schema đổi)
- FEATURE_CHECKLIST.md (nếu feature hoàn thành/đổi trạng thái)

---

## 7. VAI TRÒ AGENT GỢI Ý

### 7.1 Architect Agent
- đọc rules và kiến trúc
- kiểm tra cấu trúc module
- đề xuất cách triển khai đúng chuẩn

### 7.2 Feature Agent
- triển khai feature theo checklist
- làm đúng tầng và đúng workflow

### 7.3 Review Agent
- phát hiện lỗi nghiệp vụ, bảo mật, permission, performance
- đối chiếu với docs và requirement

### 7.4 Documentation Agent
- cập nhật changelog
- cập nhật checklist
- ghi nhận lessons learned

---

## 8. BLUEPRINT TÁI SỬ DỤNG CHO CÁC DỰ ÁN KHÁC

Mẫu này có thể áp dụng cho bất kỳ dự án nào bằng cách thay thế 3 phần:

1. Docs set
   - architecture
   - workflow
   - feature checklist
   - changelog
   - schema

2. Rules set
   - architecture rule
   - coding standard
   - security rule
   - review rule

3. Workflow set
   - backend-first / frontend-second
   - handoff rule
   - verification rule

Nếu một dự án chưa có docs, agent nên đề xuất tạo các file này trước khi code.

---

## 9. PROMPT MẪU CHO AGENT

Khi dùng agent, nên dùng prompt sau:

"Đọc toàn bộ docs/ trước khi làm bất kỳ việc gì. Không đoán. Nếu có ambiguity, hỏi lại. Tuân thủ kiến trúc và checklist. Trước khi code, viết plan ngắn. Sau khi code, chạy verify và báo cáo kết quả với evidence."

---

## 10. KẾT LUẬN

Blueprint này nhằm biến AI từ một công cụ viết code thành một trợ lý phát triển thực sự:

- hiểu context
- tuân thủ architecture
- làm việc đúng workflow
- bảo vệ chất lượng và bảo mật
- có thể tái sử dụng cho nhiều dự án khác
