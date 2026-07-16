# 🎓 AGENTS.md — Project: Student Management System
# Đặt file này tại: [project-root]/AGENTS.md
# File này override / bổ sung cho ~/.gemini/AGENTS.md (global rules vẫn còn hiệu lực)

---

## PHẦN 1: CONTEXT DỰ ÁN

### 1.1 Tổng quan
- **Tên:** Hệ thống Quản lý Sinh viên
- **Stack:** Python 3.12, Django 5.x, DRF, PostgreSQL, Redis, Celery, Docker Compose
- **Kiến trúc:** Modular Monolith — 9 apps Django độc lập, giao tiếp qua Service layer
- **Team:** 1-2 người
- **Trạng thái hiện tại:** [🔄 Cập nhật khi project tiến triển]
  - [x] ERD hoàn thành (~98%)
  - [x] Kiến trúc modular monolith xác định
  - [x] Django project scaffold, Docker Compose
  - [ ] Implement `accounts` module
  - [ ] Implement `master_data` module
  - [ ] ...

### 1.2 Cấu trúc 9 Modules (build theo thứ tự dependency)

```
Tier 1 — Foundation (không phụ thuộc gì):
  1. accounts        — Auth, User, Role, Permission
  2. master_data     — Khoa, Ngành, Học kỳ, Phòng học...

Tier 2 — Core (phụ thuộc Tier 1):
  3. students        — Hồ sơ sinh viên, trạng thái học tập
  4. academics       — Môn học, Chương trình đào tạo

Tier 3 — Operations (phụ thuộc Tier 1 + 2):
  5. enrollment      — Đăng ký môn học, lớp học phần
  6. grading         — Điểm số, GPA, kết quả học tập

Tier 4 — Extended (phụ thuộc nhiều tier trên):
  7. scheduling      — Thời khóa biểu, phân công giảng viên
  8. finance         — Học phí, miễn giảm, công nợ
  9. reporting       — Báo cáo tổng hợp, thống kê
```

### 1.3 Tech Stack chi tiết

```
Backend:
  - Django 5.x + Django REST Framework
  - SimpleJWT (access: 30 phút, refresh: 7 ngày)
  - django-filter, drf-spectacular (API docs)
  - Celery + Redis (async tasks)

Database:
  - PostgreSQL (primary)
  - Redis (cache, session, Celery broker)

DevOps:
  - Docker + Docker Compose
  - Biến môi trường qua .env (không commit)

Testing:
  - pytest-django
  - factory_boy (test fixtures)
```

---

## PHẦN 2: QUY ĐỊNH ĐẶC THÙ DỰ ÁN NÀY

### 2.1 Cấu trúc thư mục mỗi app

```
[app_name]/
├── models.py          # Model definitions only
├── serializers.py     # Input/Output serializers
├── views.py           # Thin views
├── urls.py            # URL routing
├── services.py        # Business logic (hoặc services/ folder nếu nhiều)
├── selectors.py       # Complex queries
├── permissions.py     # App-specific permissions
├── tasks.py           # Celery tasks (thin wrappers)
├── signals.py         # Django signals (side-effects đơn giản)
├── admin.py           # Django admin
└── tests/
    ├── test_services.py
    ├── test_selectors.py
    └── test_api.py
```

### 2.2 Role hệ thống

```python
class UserRole(models.TextChoices):
    ADMIN           = 'admin',          'Quản trị viên'
    ACADEMIC_STAFF  = 'academic_staff', 'Cán bộ đào tạo'
    LECTURER        = 'lecturer',       'Giảng viên'
    STUDENT         = 'student',        'Sinh viên'
```

Khi viết permission logic, LUÔN check qua Permission class — không inline trong View.

### 2.3 API Conventions

- Base URL: `/api/v1/`
- Response format thành công:
  ```json
  {
    "success": true,
    "data": { ... },
    "message": "..."
  }
  ```
- Response format lỗi:
  ```json
  {
    "success": false,
    "error": {
      "code": "VALIDATION_ERROR",
      "message": "...",
      "details": { ... }
    }
  }
  ```
- Pagination: dùng `PageNumberPagination`, default 20 items/page.
- Rate limiting: 100 requests/min per user.

### 2.4 Business Rules cần nhớ

> [🔄 Cập nhật liên tục khi có rule mới được xác định]

- Sinh viên chỉ đăng ký được môn học nếu đã hoàn thành môn tiên quyết.
- GPA tính theo thang 4.0 (có thể kèm thang 10).
- Học phí tính theo tín chỉ đăng ký trong học kỳ.
- Kết quả học tập bị khóa sau khi giảng viên submit — cần quy trình phúc khảo riêng.
- [Thêm rule mới ở đây khi phát sinh]

### 2.5 Tiêu chuẩn Comment & Docstring
- **Bắt buộc 100%:** Ở đầu mỗi file code (VD: `models.py`, `services.py`), phải có một docstring tóm tắt file này dùng để làm gì.
- **Giải thích chi tiết (Dành cho người mới học):** Trong các hàm, đoạn logic, cần phải có comment giải thích chi tiết dòng code đó đang làm gì (What) và lý do tại sao lại viết như vậy (Why). Mục đích là để cả những bạn dev mới hoặc người chưa thạo code đọc vào cũng có thể học và hiểu được luồng nghiệp vụ.
- **Type hinting:** Mọi hàm (function/method) đều phải có type hint rõ ràng ở tham số và giá trị trả về để dễ đọc.

---

## PHẦN 3: HƯỚNG DẪN THEO GIAI ĐOẠN

### 3.1 Khi nhận task ideation (`/idea`)

1. Đặt 2-3 câu hỏi làm rõ scope, actor, edge cases.
2. Phác thảo user stories theo format:
   ```
   Là [actor], tôi muốn [hành động] để [mục tiêu].
   Điều kiện chấp nhận:
   - [ ] ...
   ```
3. Chưa đề xuất giải pháp kỹ thuật ở bước này.

### 3.2 Khi thiết kế DB/kiến trúc (`/design`)

1. Trình bày ERD dạng text (tên bảng, field chính, relationship).
2. Giải thích quyết định thiết kế — tại sao không theo hướng khác.
3. Hỏi confirm trước khi viết migration.
4. Luôn nhắc: "Có cần review với file ERD hiện tại ở `docs/erd/` không?"

### 3.3 Khi chia task (`/task`)

Format output chuẩn:
```markdown
## Feature: [tên feature]

**Estimate:** [X] giờ

### Ngày 1
- [ ] [subtask cụ thể, estimatable]
- [ ] [subtask cụ thể, estimatable]

### Ngày 2
- [ ] ...

### Dependency
- Cần hoàn thành trước: [module/task]
- Block: [task nào bị block bởi task này]
```

### 3.4 Khi debug (`/debug`)

Quy trình bắt buộc:
1. **Reproduce:** Xác nhận đã reproduce được lỗi.
2. **Locate:** Tracing từ error → service → selector → model.
3. **Root cause:** Giải thích tại sao xảy ra — không chỉ nói "fix dòng X".
4. **Fix:** Đề xuất fix với giải thích trade-off.
5. **Prevent:** Đề xuất cách tránh lỗi tương tự trong tương lai.

---

## PHẦN 4: FILE QUAN TRỌNG CẦN BIẾT

```
docs/
├── erd/              # ERD diagrams và schema
├── api/              # API specification
└── architecture/     # Quyết định kiến trúc (ADR)

config/
├── settings/
│   ├── base.py       # Settings chung
│   ├── development.py
│   └── production.py
└── ...

.env.example          # Template biến môi trường — KHÔNG commit .env thật
```

Trước khi implement feature mới, AI PHẢI:
1. Kiểm tra `docs/erd/` xem có liên quan đến model nào.
2. Kiểm tra module phụ thuộc đã implement chưa (xem Tier ở Phần 1).

---

## PHẦN 5: LỊCH SỬ QUYẾT ĐỊNH KIẾN TRÚC

> [🔄 Ghi lại các quyết định quan trọng để AI không đề xuất lại hướng đã bác bỏ]

| Ngày | Quyết định | Lý do |
|---|---|---|
| [date] | Dùng Modular Monolith thay vì Microservices | Team nhỏ, giảm overhead ops |
| [date] | UUID làm primary key cho tất cả model | Tránh expose sequential ID, dễ merge data |
| Hardcode `SECRET_KEY` | Bỏ quên bảo mật | Luôn dùng `os.environ.get()` |
| Token sống 1 ngày | Không đọc kỹ `rules.md` | Bám sát spec bảo mật (30 phút) |
| Logic nghiệp vụ trong Serializer | Hiểu sai ranh giới tầng | Dừng ngay việc xử lý logic tại Serializer. Chuyển sang Service. |
| Thiếu `@transaction.atomic` | Sót khi update nhiều bảng | Tự hỏi: "Hàm này có write nhiều hơn 1 bảng không?" |
| Bị N+1 Query | Quên join bảng | Mọi query có FK = bắt buộc dùng `.select_related` |
| Bỏ quên file rác | Không dọn dẹp sau test | Dọn dẹp các file `.json`, `.py` tạm trước khi git add |

---

## PHẦN 5: CÁCH HỌC VÀ PHÁT TRIỂN TIẾP (DÀNH CHO USER)
User có thể "dạy" AI thêm kỹ năng mới bằng cách:
1. Cập nhật trực tiếp file `AGENTS.md` này để nạp thêm rule (luật) mới.
2. Dùng lệnh `/learn` trong khung chat (hoặc gọi Workflow Skill Creator) để AI tự động đúc kết một quy trình phức tạp thành một **Skill** mới và lưu vào thư mục `.agents/skills/`. Lần sau chỉ cần gọi tên Skill là AI sẽ làm chuẩn xác!

---

## PHẦN 6: QUY TẮC THIẾT KẾ FRONTEND (UI/UX)
*(Bắt buộc tuân thủ khi viết code cho Frontend)*

- Bắt buộc phải đọc và làm theo file `docs/architecture/ui_guidelines.md`.
- **Công nghệ chính:** Sử dụng `shadcn/ui`, `Tailwind CSS`, `lucide-react`.
- **Tính thẩm mỹ:** Chuẩn Enterprise, tối giản, màu Indigo/Slate, font Inter/Geist.
- **UX Code:** Bắt buộc dùng Skeleton Loading khi đang tải API (bằng Tanstack Query). Xử lý form bằng `react-hook-form` + `zod`.
- **Phản hồi:** Thêm, Sửa, Xóa thành công phải bắn Toast Notification thay vì Alert.

