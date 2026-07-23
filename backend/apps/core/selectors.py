from .models import SystemConfig, AuditLog

class SystemConfigSelector:
    @staticmethod
    def get_configs():
        return SystemConfig.objects.all()

    @staticmethod
    def get_lockout_config():
        """
        Lấy cấu hình lockout từ database, trả về (max_attempts, lockout_duration_minutes)
        """
        try:
            max_attempts = int(SystemConfig.objects.get(key='MAX_LOGIN_ATTEMPTS').value)
        except (SystemConfig.DoesNotExist, ValueError):
            max_attempts = 5

        try:
            lockout_duration = int(SystemConfig.objects.get(key='LOCKOUT_DURATION_MINUTES').value)
        except (SystemConfig.DoesNotExist, ValueError):
            lockout_duration = 15

        return max_attempts, lockout_duration

class AuditLogSelector:
    @staticmethod
    def get_logs():
        # Dùng select_related('user') để tránh N+1 Query
        return AuditLog.objects.select_related('user').all()
