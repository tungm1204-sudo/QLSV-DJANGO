"""
config/settings/development.py
Cấu hình Django CHỈ DÀNH CHO môi trường DEVELOPMENT (máy local của developer).
Lý do: Cho phép DEBUG=True, CORS mở rộng để dev dễ làm việc mà không ảnh hưởng production.

Cách dùng:
  - Trong .env, đặt: DJANGO_SETTINGS_MODULE=config.settings.development
  - Hoặc chạy: python manage.py runserver --settings=config.settings.development
"""

# Import toàn bộ cấu hình chung từ base.py
from .base import *

# --- DEBUG MODE ---
# DEBUG=True sẽ hiển thị traceback lỗi chi tiết trên trình duyệt.
# Lý do: Giúp developer tìm lỗi nhanh. TUYỆT ĐỐI không bật ở production.
DEBUG = True

# Khi DEBUG=True, Django cho phép mọi host.
# Lý do: Cho phép dev dùng localhost, 127.0.0.1 mà không cần cấu hình thêm.
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# --- CORS ---
# Cho phép frontend (React/Vite chạy ở port 5173) gọi API và gửi kèm Cookie (withCredentials).
# Lý do: HTTPOnly Cookie cần CORS cụ thể thay vì ALLOW_ALL để hoạt động bảo mật.
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
CORS_ALLOW_CREDENTIALS = True

# --- LOGGING (tùy chọn) ---
# Hiển thị câu lệnh SQL ra console khi dev để debug query N+1.
# Bỏ comment dòng dưới nếu muốn xem SQL đang chạy:
# LOGGING = {
#     'version': 1,
#     'handlers': {'console': {'class': 'logging.StreamHandler'}},
#     'loggers': {'django.db.backends': {'handlers': ['console'], 'level': 'DEBUG'}},
# }
