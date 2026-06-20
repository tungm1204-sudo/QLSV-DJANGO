# AI Agents & Project Bootstrap Guide

Tài liệu này được thiết kế như một **System Prompt / Knowledge Base** dành cho các AI Agents (như Antigravity, GitHub Copilot, Cursor, v.v.) khi tham gia vào dự án này, hoặc khi bạn (User) muốn tái sử dụng bộ khung (boilerplate) này cho một dự án mới.

## 1. Vai trò của AI Agent
Khi làm việc trên dự án này (hoặc dự án clone từ đây), AI Agent cần đóng vai trò là một **Full-Stack Developer** chuyên nghiệp với tư duy **API-First** và tuân thủ chặt chẽ kiến trúc **Decoupled (Django Backend + React Frontend)**.

## 2. Tech Stack Core (Bắt buộc tuân thủ)
Bất kỳ tính năng mới nào được thêm vào đều phải sử dụng các công nghệ sau:
*   **Backend:** Python, Django 6.x, Django REST Framework (DRF), SimpleJWT, PostgreSQL (hoặc SQLite môi trường dev).
*   **Frontend:** Vite, React, Tailwind CSS, shadcn/ui, Zustand (Global State), TanStack React Query v5 (Data Fetching).
*   **Testing:** `pytest` và `pytest-django` (Backend).

## 3. Quy ước cấu trúc thư mục & Code (Coding Conventions)

### Dành cho Backend (Django)
1.  **App-based structure:** Mỗi domain logic phải nằm trong một app riêng biệt (VD: `accounts`, `core`, v.v.).
2.  **Fat Models, Thin Views:** Chứa business logic trong Model methods hoặc Services, tránh nhồi nhét logic vào Views.
3.  **DRF Standards:** Sử dụng `ModelViewSet` và `Serializer` để chuẩn hóa API. Tuân thủ RESTful routing (e.g., `/api/v1/resources/`).
4.  **Phân quyền (Permissions):** Luôn kiểm tra permission tại cả mức View và Object (nếu cần). Sử dụng Custom Permissions khi logic phức tạp.

### Dành cho Frontend (React)
1.  **Feature-based architecture:** Code được chia theo module trong `src/features/`. Trong mỗi feature folder nên có:
    *   `api.js`: Định nghĩa các API calls sử dụng `axiosClient`.
    *   `hooks.js`: Chứa custom hooks dùng React Query (VD: `useItems()`, `useCreateItem()`).
    *   `components/`: Các components UI cụ thể cho feature đó.
2.  **UI Components:** Tái sử dụng tối đa các atomic components từ `src/components/ui/` (được xây dựng bằng shadcn/ui). Không viết lại CSS thủ công nếu Tailwind đã hỗ trợ.
3.  **State Management:** State của server (dữ liệu API) phải được quản lý bởi **React Query**. Chỉ dùng **Zustand** cho các global client state (như User Auth, UI Theme, Sidebar Toggle).

## 4. Quy trình thêm tính năng mới (Workflow Step-by-Step cho AI)

Mỗi khi user yêu cầu tạo một module/tính năng mới, AI cần phải thực hiện theo trình tự sau:

**Bước 1: Thiết kế Backend API**
- Định nghĩa Database Model (`models.py`).
- Viết API Serializer (`serializers.py`).
- Tạo ViewSet xử lý logic CRUD (`views.py`).
- Định nghĩa Routing (`urls.py`).
- (Tuỳ chọn) Viết Unit Test cơ bản bằng `pytest` (`tests/`).

**Bước 2: Cập nhật & Kiểm thử Backend**
- Hỗ trợ User tạo file migration và apply db (`makemigrations`, `migrate`).
- Đảm bảo API trả về đúng format JSON chuẩn và xử lý tốt các HTTP Status Codes (200, 201, 400, 404, 403).

**Bước 3: Tích hợp Frontend**
- Tạo thư mục feature mới trong `src/features/`.
- Định nghĩa file `api.js` gọi API từ backend thông qua file setup `axiosClient` có sẵn.
- Tạo file `hooks.js` bọc các API calls bằng `useQuery` và `useMutation`.
- Xây dựng giao diện List/Form sử dụng các component của shadcn/ui hiện có.
- Liên kết giao diện mới với Router (trong `App.jsx` hoặc file quản lý Route tương tự).

**Bước 4: Test & Verify (Bắt buộc)**
- Sau khi hoàn thành việc viết code cho bất kỳ task nào, AI **phải** chạy các lệnh kiểm thử (ví dụ: `pytest` cho backend, kiểm tra build/lint cho frontend) hoặc chạy thử local server để đảm bảo không có lỗi cú pháp, lỗi logic trước khi báo cáo cho User. Không bao giờ bàn giao code mà chưa xác nhận nó có thể chạy được.

## 5. Hướng dẫn Tái sử dụng (Dành cho User khi tạo Project mới)

Để dùng project này làm template cho một dự án mới hoàn toàn:
1. Clone / Copy lại toàn bộ thư mục này.
2. **Xóa các app nghiệp vụ cũ** (nếu không cần thiết) ở Backend (như `students`, `teachers`, `academics` ở project QLSV cũ).
3. Gỡ khai báo các app đã xóa khỏi `INSTALLED_APPS` trong `settings.py`.
4. Xóa thư mục con trong `src/features/` và các trang (pages) cũ ở Frontend.
5. Cập nhật lại Navigation / Sidebar và Router bên Frontend.
6. Xóa `db.sqlite3` cũ, xóa nội dung trong các thư mục `migrations` (giữ lại file `__init__.py`).
7. Mở file `AGENTS.md` này và cung cấp (prompt) cho AI: 
   > *"Dự án này là một boilerplate sử dụng kiến trúc như trong AGENTS.md. Hãy đóng vai trò AI Agent được mô tả trong đó và tạo cho tôi module [Tên Module Mới]."*

---
**🚀 Lời nhắc chung cho AI:** Khi được yêu cầu viết code, hãy luôn ưu tiên **tính ổn định, dễ bảo trì, tính tái sử dụng cao** và **thiết kế UI đẹp mắt, trải nghiệm người dùng hiện đại** (Responsive, loading states, error boundaries, micro-animations).
