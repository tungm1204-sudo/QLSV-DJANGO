# QUY TẮC BẮT BUỘC CHO AI AGENT (devA)
> Được tạo sau khi phân tích lỗi ngày 2026-07-13. Bắt buộc tuân thủ trước mỗi lần commit.

---

## DANH SÁCH KIỂM TRA TRƯỚC KHI COMMIT (KHÔNG ĐƯỢC BỎ QUA)

### 1. Bảo mật (Security)
- [ ] Không có `SECRET_KEY`, password, token, connection string nào nằm trong file `.py` hoặc file code
- [ ] Tất cả secret đọc từ `os.environ` hoặc `python-dotenv`
- [ ] Không có `code_for_testing` hoặc data nhạy cảm trong response (trừ khi `settings.DEBUG=True`)
- [ ] Không có file rác: `excel_out.json`, `test_api.py`, `create_superuser.py`, `seed_*.py`, `*.log`

### 2. Cấu hình (Configuration — rules.md Mục 6)
- [ ] `ACCESS_TOKEN_LIFETIME = timedelta(minutes=30)` — không phải ngày, không phải giờ
- [ ] `REFRESH_TOKEN_LIFETIME = timedelta(days=7)`
- [ ] Rate limiting đã được cấu hình: `anon=20/min`, `user=100/min`
- [ ] Phân trang `PAGE_SIZE=20` đã được đặt

### 3. Model (rules.md Mục 4)
- [ ] **TẤT CẢ** model đều có `id = UUIDField(primary_key=True, ...)` — không có ngoại lệ
- [ ] **TẤT CẢ** `ForeignKey` đều có `related_name='...'` được khai báo rõ
- [ ] **TẤT CẢ** `ForeignKey` đều có `on_delete=...` được khai báo rõ

### 4. Service Layer (rules.md Mục 4) — ĐÂY LÀ ĐIỂM HAY MẮC LỖI NHẤT
- [ ] **View** chỉ làm: nhận request → gọi `serializer.is_valid()` → trích xuất `ip`, `user_agent` → gọi Service → trả Response. **Không có gì khác.**
- [ ] **Serializer** chỉ làm: khai báo field, validate format. **Không được gọi Service, không được gọi Model trực tiếp để tạo/sửa dữ liệu.**
- [ ] **Service** không nhận `request` object. Chỉ nhận dữ liệu primitive (string, dict, Model instance).
- [ ] **Service** không import View hoặc Serializer.
- [ ] Mọi hàm Service ghi vào **nhiều hơn 1 bảng** đều phải có `@transaction.atomic`.

### 5. Performance (rules.md Mục 4)
- [ ] **TẤT CẢ** selector query có ForeignKey đều dùng `.select_related()` hoặc `.prefetch_related()`
- [ ] Không có query DB dư thừa trong View (ví dụ: đừng query lại user sau khi serializer đã load user)

### 6. Test
- [ ] Chạy `python manage.py test [app]` → phải PASS 100%
- [ ] Chạy `python manage.py check` → không có issue

---

## CÁC LỖI ĐÃ MẮC PHẢI — GHI NHỚ ĐỂ KHÔNG TÁI PHẠM

| Lỗi | Nguyên nhân | Cách phòng tránh |
|---|---|---|
| `SECRET_KEY` hardcode trong `settings.py` | Không nghĩ đến bảo mật | Luôn dùng `os.environ.get()` |
| `ACCESS_TOKEN_LIFETIME = 1 day` | Không đọc kỹ `rules.md` | Kiểm tra checklist bảo mật |
| Business logic trong Serializer | Hiểu sai ranh giới tầng | Serializer = khai báo field. Stop. |
| `@transaction.atomic` thiếu | Chỉ thêm vào chỗ "rõ ràng", bỏ sót hàm ghi nhiều bảng | Hỏi: "Hàm này có ghi >1 bảng không?" |
| N+1 query trong selectors | Quên `select_related` | Mọi query có FK = phải có `select_related` |
| `excel_out.json` commit vào repo | Không dọn dẹp sau khi test | Chạy checklist "file rác" trước commit |
| `SystemConfig` dùng CharField PK | Áp dụng UUID không nhất quán | Scan **TẤT CẢ** model sau khi thêm model mới |
| `AuditLog` thiếu `related_name` | Áp dụng FK rule không nhất quán | Scan **TẤT CẢ** ForeignKey sau khi thêm model |
| OTP không filter theo `type` | Implement thiếu logic nghiệp vụ | Đọc kỹ nghiệp vụ, hỏi "OTP này dùng để làm gì?" |
| `code_for_testing` lộ ra production | Không nghĩ đến môi trường production | Guard bằng `if settings.DEBUG` |

---

## QUY TẮC GIAO TIẾP

- **KHÔNG báo cáo "xong"** nếu chưa chạy qua toàn bộ checklist ở trên
- **KHÔNG commit** nếu còn file rác, hardcoded secret, hoặc test fail
- **Báo cáo phải rõ ràng**: nêu test nào đã chạy, kết quả là gì, commit hash là gì
