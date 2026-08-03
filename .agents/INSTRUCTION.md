# 🛠️ INSTRUCTION NGẮN CHO COPILOT / AGENT

Dùng file này khi làm việc với dự án QLSV-DJANGO.

## Quy tắc bắt buộc
- Đọc toàn bộ thư mục docs/ trước khi làm bất kỳ task nào.
- Không đoán tên field, status, API, hay logic nghiệp vụ.
- Tuân thủ kiến trúc Service Layer: View mỏng, Service dày, Selector cho query, Serializer cho validate.
- Nếu task có liên quan đến permission, bảo mật, transaction, hoặc logic nghiệp vụ, phải kiểm tra kỹ trước khi sửa.
- Trước khi code, viết implementation plan ngắn.
- Sau khi code, chạy verify và báo cáo bằng evidence.

## Khi làm task
1. Đọc yêu cầu và docs liên quan.
2. Đối chiếu với FEATURE_CHECKLIST.md.
3. Xác định module, file liên quan, và test cần chạy.
4. Code đúng tầng và đúng quy chuẩn.
5. Verify bằng test/check thực tế.

## Khi phát hiện bug
- Xác định nguyên nhân.
- Đánh giá impact.
- Fix tối thiểu.
- Thêm test hoặc case kiểm thử nếu cần.

## Khi hoàn thành
- Nêu rõ task đã làm.
- Liệt kê file đã sửa.
- Nêu kết quả verify.
- Nếu có thay đổi API/schema, cập nhật changelog.
