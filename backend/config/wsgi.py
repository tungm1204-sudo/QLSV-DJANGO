"""
config/wsgi.py
Diểm vào của ứng dụng Django theo giao thức WSGI (Web Server Gateway Interface).
Lý do: Server thật (Gunicorn, uWSGI) sử dụng file này để chạy ứng dụng Django.
"""

import os

from django.core.wsgi import get_wsgi_application

# Trên server production, biến DJANGO_SETTINGS_MODULE phải được đặt sẵn trong file .env
# với giá trị là 'config.settings.production'.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

application = get_wsgi_application()
