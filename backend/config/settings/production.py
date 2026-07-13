"""
config/settings/production.py
Cấu hình Django CHỈ DÀNH CHO môi trường PRODUCTION (server thật).
Lý do: Tắt DEBUG, giới hạn CORS và ALLOWED_HOSTS để đảm bảo bảo mật khi deploy.

Cách dùng:
  - Trong .env trên server, đặt: DJANGO_SETTINGS_MODULE=config.settings.production
  - Đồng thời đặt: ALLOWED_HOSTS=yourdomain.com và CORS_ALLOWED_ORIGINS=https://yourdomain.com
"""

import os
# Import toàn bộ cấu hình chung từ base.py
from .base import *

# --- DEBUG ---
# TUYỆT ĐỐI phải là False ở production.
# Lý do: DEBUG=True sẽ lộ toàn bộ source code, biến môi trường và cấu trúc DB
# ra ngoài khi có lỗi — đây là lỗ hổng bảo mật nghiêm trọng nhất.
DEBUG = False

# --- ALLOWED_HOSTS ---
# Chỉ chấp nhận request từ domain chính thức của dự án.
# Lý do: Ngăn chặn HTTP Host Header Attack.
# Đặt trong .env: ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
_allowed = os.environ.get('ALLOWED_HOSTS', '')
ALLOWED_HOSTS = [host.strip() for host in _allowed.split(',') if host.strip()]

# --- CORS ---
# Chỉ cho phép Frontend domain chính thức gọi API.
# Lý do: Ngăn các website lạ gọi API của mình (Cross-Site Request Forgery).
# Đặt trong .env: CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
_cors = os.environ.get('CORS_ALLOWED_ORIGINS', '')
CORS_ALLOWED_ORIGINS = [origin.strip() for origin in _cors.split(',') if origin.strip()]

# --- SECURITY HEADERS ---
# Bật các HTTP Header bảo mật để chống các loại tấn công phổ biến trên trình duyệt.

# Bắt buộc trình duyệt kết nối qua HTTPS, không chấp nhận HTTP.
SECURE_SSL_REDIRECT = True

# Bảo vệ Cookie không bị gửi qua kết nối HTTP thường.
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# HSTS: Yêu cầu trình duyệt ghi nhớ chỉ dùng HTTPS trong 1 năm.
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Ngăn trình duyệt đoán mò Content-Type (chống MIME-sniffing attack).
SECURE_CONTENT_TYPE_NOSNIFF = True
