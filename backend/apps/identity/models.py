"""
Module Identity Models
Định nghĩa các cấu trúc cơ sở dữ liệu (Models) cho phân hệ Quản lý Danh tính và Phân quyền (Tier 1).
Bao gồm: User, Role, LoginSession, SystemConfig, OTPToken, AuditLog, Notification.
Lý do: Tách biệt hoàn toàn phần xác thực khỏi logic nghiệp vụ để tập trung kiểm soát bảo mật và phân quyền.
"""

import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class UserManager(BaseUserManager):
    """
    Tùy chỉnh Manager cho User model để hỗ trợ đăng nhập bằng Email thay vì Username mặc định của Django.
    """
    def create_user(self, email: str, password: str = None, **extra_fields) -> 'User':
        if not email:
            raise ValueError('Email address is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('status', 'ACTIVE')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class Role(models.Model):
    """
    Model định nghĩa Vai trò (Role) trong hệ thống và danh sách các quyền (permissions) tương ứng.
    Lý do dùng JSONField cho permissions: Tối ưu tốc độ query và linh hoạt khi mở rộng quyền mới mà không cần join bảng.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    permissions = models.JSONField(default=list, blank=True) # list of string permissions
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'identity_roles'
        ordering = ['name']

    def __str__(self):
        return self.name

class User(AbstractBaseUser, PermissionsMixin):
    """
    Model lưu trữ thông tin tài khoản người dùng chính của toàn hệ thống (Student, Lecturer, Admin,...).
    Sử dụng UUID làm khóa chính theo chuẩn dự án để tránh rò rỉ ID tuần tự (ngăn chặn tấn công IDOR).
    """
    class StatusChoices(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Active'
        INACTIVE = 'INACTIVE', 'Inactive'
        LOCKED = 'LOCKED', 'Locked'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, max_length=255)
    full_name = models.CharField(max_length=255)
    avatar = models.URLField(max_length=1000, blank=True, null=True)
    
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.ACTIVE)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True, related_name='users')
    
    # Account lockout logic
    failed_login_attempts = models.IntegerField(default=0)
    locked_until = models.DateTimeField(null=True, blank=True)
    
    # Required fields for Django admin and authentication
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True) # Usually tied to status but kept for django compat
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    class Meta:
        db_table = 'identity_users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.email} ({self.full_name})"

class LoginSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='login_sessions')
    token_jti = models.CharField(max_length=255, unique=True, null=True, blank=True) # ID của refresh token
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    device_info = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'identity_login_sessions'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.created_at}"

class SystemConfig(models.Model):
    """
    Model lưu trữ các cấu hình động của hệ thống (như: thời gian hết hạn OTP, số lần login sai tối đa).
    Lý do: Cho phép Admin thay đổi cấu hình nóng (hot-reload) từ UI mà không cần restart lại ứng dụng hay sửa file code.
    """
    # Fix #12: UUID PK thay vì CharField PK theo rules.md
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    key = models.CharField(max_length=100, unique=True)
    value = models.JSONField()
    description = models.TextField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'identity_system_configs'

    def __str__(self):
        return self.key

class OTPToken(models.Model):
    class TypeChoices(models.TextChoices):
        LOGIN = 'LOGIN', 'Login'
        PASSWORD_RESET = 'PASSWORD_RESET', 'Password Reset'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otp_tokens')
    code = models.CharField(max_length=10)
    type = models.CharField(max_length=20, choices=TypeChoices.choices, default=TypeChoices.LOGIN)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'identity_otp_tokens'
        indexes = [
            models.Index(fields=['user', 'code', 'type', 'is_used']),
        ]

    def is_valid(self):
        return not self.is_used and timezone.now() <= self.expires_at

class AuditLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Fix #13: Thêm related_name theo rules.md
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='audit_logs')
    action = models.CharField(max_length=50) # CREATE, UPDATE, DELETE, LOGIN
    module = models.CharField(max_length=100) # e.g. Users, Roles
    record_id = models.CharField(max_length=255, null=True, blank=True)
    payload = models.JSONField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'identity_audit_logs'
        ordering = ['-created_at']

class Notification(models.Model):
    class TypeChoices(models.TextChoices):
        INFO = 'INFO', 'Info'
        WARNING = 'WARNING', 'Warning'
        SUCCESS = 'SUCCESS', 'Success'
        ERROR = 'ERROR', 'Error'
        SYSTEM = 'SYSTEM', 'System'
        GRADE = 'GRADE', 'Grade'
        TUITION = 'TUITION', 'Tuition'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications') # null means broadcast
    title = models.CharField(max_length=255)
    message = models.TextField()
    type = models.CharField(max_length=20, choices=TypeChoices.choices, default=TypeChoices.INFO)
    
    # Dùng GenericForeignKey để định tuyến
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.CharField(max_length=255, null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'identity_notifications'
        ordering = ['-created_at']

