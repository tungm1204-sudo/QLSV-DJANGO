"""
config/settings/base.py
Cấu hình Django DÙNG CHUNG cho tất cả môi trường (development, production).
Lý do tách ra file riêng: Tránh trùng lặp code giữa các môi trường, mọi thay đổi
cốt lõi chỉ cần sửa ở đây.

QUAN TRỌNG: File này KHÔNG được import trực tiếp vào manage.py hay wsgi.py.
Thay vào đó, hãy dùng config.settings.development hoặc config.settings.production.
"""

from pathlib import Path
from datetime import timedelta
import os
from dotenv import load_dotenv
import dj_database_url

# Tìm và nạp file .env từ thư mục backend/ (thư mục cha của config/)
load_dotenv()

# BASE_DIR trỏ đến thư mục backend/ — dùng để build đường dẫn tuyệt đối
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# --- SECURITY ---
# SECRET_KEY bắt buộc phải đặt trong .env, không được hardcode.
# Lý do: Nếu lộ SECRET_KEY, hacker có thể giả mạo session và JWT token.
SECRET_KEY = os.environ.get('SECRET_KEY')

# --- DATABASE ---
# Đọc chuỗi kết nối DB từ biến môi trường DATABASE_URL trong file .env.
# Lý do: Không hardcode thông tin kết nối DB để đảm bảo bảo mật và linh hoạt giữa các môi trường.
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get("DATABASE_URL"),
        # conn_max_age=600 nghĩa là giữ kết nối DB trong 10 phút thay vì đóng sau mỗi request.
        # Lý do: Tối ưu hiệu năng, giảm thời gian overhead tạo kết nối mới.
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# --- INSTALLED APPS ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'django_filters',
    'corsheaders',
    'drf_spectacular',

    # Local apps — thêm module mới vào đây khi build
    'apps.identity',
    'apps.master_data',
    'apps.curriculum',
    'apps.affairs',
    'apps.hr',
    # 'apps.students',
    'apps.enrollment',
    # 'apps.grading',
    # 'apps.scheduling',
    # 'apps.finance',
    # 'apps.reporting',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # CORS phải đứng trước CommonMiddleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# --- PASSWORD VALIDATION ---
# Django tự động kiểm tra mật khẩu theo các rule này khi gọi set_password().
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 8},
    },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- INTERNATIONALIZATION ---
LANGUAGE_CODE = 'en-us'
# TIME_ZONE dùng UTC để tránh nhầm lẫn múi giờ khi lưu vào DB.
# Lý do: Postgres lưu timestamp theo UTC, nếu để timezone khác sẽ gây lỗi so sánh giờ.
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# --- STATIC FILES ---
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- CUSTOM USER MODEL ---
# Khai báo để Django biết dùng model User trong app 'identity' thay vì User mặc định.
AUTH_USER_MODEL = 'identity.User'

# --- DJANGO REST FRAMEWORK ---
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ),
    # Phân trang mặc định: 20 items/trang
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    # Mặc định mọi API đều yêu cầu đăng nhập.
    # Lý do: Bảo mật theo hướng "deny by default" — phải khai báo rõ AllowAny nếu muốn public.
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    # Rate Limiting: Giới hạn số request để chống DDoS và bot.
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '20/min',   # Anonymous user: 20 request/phút
        'user': '100/min',  # Logged-in user: 100 request/phút
    },
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# --- SWAGGER SPECTACULAR ---
SPECTACULAR_SETTINGS = {
    'TITLE': 'QLSV API',
    'DESCRIPTION': 'Tài liệu API cho Hệ thống Quản lý Sinh viên',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    # Cấu hình UI
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        'persistAuthorization': True,
        'displayOperationId': True,
    },
}

# --- SIMPLE JWT ---
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),  # Hết hạn sau 30 phút
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),      # Hết hạn sau 7 ngày
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_COOKIE_REFRESH': 'refresh_token',
}
