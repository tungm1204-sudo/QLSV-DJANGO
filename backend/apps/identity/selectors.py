from django.contrib.auth import get_user_model
from .models import LoginSession, Notification, OTPToken, AuditLog

User = get_user_model()

class AuthSelector:
    @staticmethod
    def get_login_sessions(user):
        return LoginSession.objects.filter(user=user).order_by('-created_at')[:50]
        
class UserSelector:
    @staticmethod
    def get_user_by_email(email):
        return User.objects.filter(email=email).first()

class NotificationSelector:
    @staticmethod
    def get_user_notifications(user):
        return Notification.objects.filter(user=user).order_by('-created_at')

class AuditLogSelector:
    @staticmethod
    def get_logs():
        return AuditLog.objects.all().order_by('-created_at')
