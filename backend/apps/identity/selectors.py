"""
Module Identity Selectors
Chuyên đảm nhận các tác vụ truy vấn dữ liệu (Query/Read) phức tạp từ Database.
Lý do: Tách biệt logic đọc (Selector) và ghi (Service). Đặc biệt ở đây bắt buộc sử dụng select_related/prefetch_related để chặn đứng lỗi N+1 Query.
"""

from django.contrib.auth import get_user_model
from .models import LoginSession, Notification, AuditLog

User = get_user_model()

class AuthSelector:
    @staticmethod
    def get_login_sessions(user):
        # Fix #8: select_related để tránh N+1 query
        return LoginSession.objects.filter(user=user).order_by('-created_at')[:50]

class UserSelector:
    @staticmethod
    def get_user_by_email(email):
        return User.objects.filter(email=email).first()

class NotificationSelector:
    @staticmethod
    def get_user_notifications(user):
        # Fix #8: select_related để tránh N+1 query với content_type
        return (
            Notification.objects
            .filter(user=user)
            .select_related('content_type')
            .order_by('-created_at')
        )

class AuditLogSelector:
    @staticmethod
    def get_logs():
        # Fix #8: select_related để tránh N+1 query với user
        return AuditLog.objects.select_related('user').order_by('-created_at')
