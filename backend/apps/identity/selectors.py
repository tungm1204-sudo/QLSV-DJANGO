"""
Module Identity Selectors
Chuyên đảm nhận các tác vụ truy vấn dữ liệu (Query/Read) phức tạp từ Database.
Lý do: Tách biệt logic đọc (Selector) và ghi (Service). Đặc biệt ở đây bắt buộc sử dụng select_related/prefetch_related để chặn đứng lỗi N+1 Query.
"""

from django.contrib.auth import get_user_model
from .models import LoginSession

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

