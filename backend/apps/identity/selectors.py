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
        # Lấy lịch sử đăng nhập của user, sắp xếp mới nhất lên đầu, giới hạn 50 records.
        # Lý do giới hạn [:50]: Tránh việc load hàng ngàn record làm tràn RAM server và chậm API.
        return LoginSession.objects.filter(user=user).order_by('-created_at')[:50]

class UserSelector:
    @staticmethod
    def get_user_by_email(email):
        return User.objects.filter(email=email).first()

class NotificationSelector:
    @staticmethod
    def get_user_notifications(user):
        # Lấy danh sách thông báo của người dùng.
        # Fix #8: BẮT BUỘC dùng select_related('content_type').
        # Lý do: Khi Serializer bóc dữ liệu ra, nếu không có select_related, mỗi dòng notification sẽ sinh ra 1 câu query phụ để lấy thông tin content_type. Gây ra thảm họa N+1 Query làm nghẽn DB.
        return (
            Notification.objects
            .filter(user=user)
            .select_related('content_type')
            .order_by('-created_at')
        )

class AuditLogSelector:
    @staticmethod
    def get_logs():
        # Lấy toàn bộ lịch sử thao tác của hệ thống.
        # BẮT BUỘC dùng select_related('user').
        # Lý do: Giúp Django tạo ra câu lệnh SQL có JOIN ngay từ đầu, lấy luôn thông tin User thay vì query riêng lẻ từng User cho mỗi dòng AuditLog.
        return AuditLog.objects.select_related('user').order_by('-created_at')
