# 🎓 HỆ THỐNG QUẢN LÝ SINH VIÊN (SIS)

Hệ thống thông tin sinh viên toàn diện xây dựng theo chuẩn **Django REST Framework (Backend)** và **React (Frontend)**, áp dụng chặt chẽ kiến trúc **Service Layer**.

## 📚 TÀI LIỆU DỰ ÁN (DOCUMENTATION)

Toàn bộ tài liệu quy trình, tiêu chuẩn code và thiết kế hệ thống đã được quy chuẩn hóa thành các file Markdown trong thư mục `docs/`.

### 1. Kiến trúc & Coding Convention
- [Quy tắc Kiến trúc (Service Layer)](docs/architecture/rules.md) - Quy định BẮT BUỘC về kiến trúc backend (View siêu mỏng, Service siêu dày), Database (UUID, Transaction), JWT và Frontend.
- [Sơ đồ Hệ thống](docs/architecture/system_diagrams.md) - Biểu đồ Use Case và luồng dữ liệu (Mermaid).

### 2. Quản lý Dự án & Tiến độ
- [Checklist Tính năng](docs/management/FEATURE_CHECKLIST.md) - 100% tính năng của hệ thống (9 Modules) dùng để tracking.
- [Quy trình Phối hợp Team](docs/management/TEAM_WORKFLOW.md) - Chiến lược phát triển Strict Sequential Handoff (Backend đi trước, Frontend theo sau), phân chia theo Khối (Block) 3 ngày/khối.

## 🤖 QUY TẮC CHO AI AGENTS

Dự án này sử dụng AI để lập trình (devA, devB). Nhằm đảm bảo AI không phá vỡ kiến trúc, không bỏ quên các quy tắc bảo mật (như hardcode Secret Key) và tuân thủ đúng yêu cầu, chúng tôi sử dụng **Customization Skills/Rules** cho Agent.

Các quy tắc cứng của dự án được nạp tự động thông qua file:
👉 [AGENTS.md](.agents/AGENTS.md) (Checklist BẮT BUỘC trước mỗi commit).

### Tái sử dụng luật cho dự án khác (Global Customization)
Nếu bạn là Developer muốn áp dụng mô hình Service Layer chuẩn mực này cho các dự án AI khác, hãy tạo thư mục `C:\Users\Admin\.gemini\config` và copy nội dung kiến trúc vào file `AGENTS.md` tại đó. Hệ thống sẽ tự động biến nó thành luật mặc định cho mọi project.

## 🚀 CÀI ĐẶT & CHẠY DỰ ÁN

### 1. Clone & Môi trường
```bash
git clone https://github.com/tungm1204-sudo/QLSV-DJANGO.git
cd QLSV-DJANGO
```

### 2. Backend (Django)
```bash
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Cấu hình biến môi trường
cp .env.example .env
# (Sửa DATABASE_URL và SECRET_KEY trong .env)

python manage.py migrate
python manage.py runserver
```

### 3. Frontend (React)
```bash
cd frontend
npm install
npm run dev
```
