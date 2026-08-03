# ✅ CHECKLIST VẬN HÀNH CHO DEVELOPER VÀ AI AGENT

Tài liệu này dùng để kiểm soát chất lượng mỗi khi làm việc với dự án.

---

## 1. TRƯỚC KHI BẮT ĐẦU TASK

- [ ] Đã đọc yêu cầu đầy đủ
- [ ] Đã đọc các file docs liên quan
- [ ] Đã xác định task thuộc module nào
- [ ] Đã đối chiếu với FEATURE_CHECKLIST
- [ ] Nếu có ambiguity, đã hỏi lại user
- [ ] Đã lập plan ngắn trước khi code

---

## 2. KHI VIẾT CODE

- [ ] Đã hiểu đúng tầng: View / Service / Selector / Serializer
- [ ] Không viết business logic thừa vào View hoặc Serializer
- [ ] Nếu thao tác nhiều bảng, đã dùng transaction
- [ ] Nếu query có FK, đã dùng select_related / prefetch_related
- [ ] Không hardcode secret/key/password
- [ ] Có docstring/comment giải thích what và why
- [ ] Đã dùng type hint cho hàm mới

---

## 3. KHI XỬ LÝ BẢO MẬT

- [ ] Đã kiểm tra permission trước khi thao tác
- [ ] Không cho phép bypass logic nghiệp vụ không có quyền
- [ ] Không trả dữ liệu nhạy cảm trong response
- [ ] Không lưu mật khẩu plaintext trong import/export
- [ ] Đã kiểm tra input validation

---

## 4. KHI HOÀN THÀNH TASK

- [ ] Đã chạy test/check phù hợp
- [ ] Đã kiểm tra lỗi syntax
- [ ] Đã kiểm tra API response
- [ ] Nếu có frontend, đã test UI thực tế
- [ ] Nếu có thay đổi schema/API, đã cập nhật changelog
- [ ] Đã cập nhật FEATURE_CHECKLIST nếu feature hoàn thành

---

## 5. KHI REVIEW CODE

- [ ] Code có đúng kiến trúc không?
- [ ] Có vi phạm rule nào không?
- [ ] Có bug nghiệp vụ hoặc bảo mật không?
- [ ] Có performance issue như N+1 query không?
- [ ] Có test case nào cần bổ sung không?

---

## 6. KHI BÁO CÁO HOÀN THÀNH

Báo cáo phải có:

- [ ] mục tiêu đã làm
- [ ] file đã chỉnh sửa
- [ ] test/check đã chạy
- [ ] kết quả thực tế
- [ ] rủi ro hoặc việc còn thiếu

---

## 7. QUY TẮC DÀNH CHO AI AGENT

- [ ] Đọc docs trước khi sửa code
- [ ] Không đoán tên field/status nếu chưa xác nhận
- [ ] Không tự ý thay đổi kiến trúc nếu chưa được xác nhận
- [ ] Nếu không chắc, dừng lại và hỏi user
- [ ] Luôn verify bằng evidence trước khi kết luận
