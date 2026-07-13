#!/usr/bin/env python
"""
manage.py
Công cụ dòng lệnh của Django để chạy server, migrate DB, tạo migration, v.v.
Lý do: Mặc định sẽ dùng settings Development khi chạy trên máy local.
Muốn dùng production settings thì đặt biến môi trường DJANGO_SETTINGS_MODULE trong .env.
"""
import os
import sys


def main():
    """Run administrative tasks."""
    # Mặc định dùng settings development khi chạy lệnh manage.py trên máy local.
    # Lý do: Tránh vô tình chạy với production settings (DEBUG=False) trên máy dev.
    # Biến DJANGO_SETTINGS_MODULE trong .env sẽ ghi đè giá trị này nếu cần.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
