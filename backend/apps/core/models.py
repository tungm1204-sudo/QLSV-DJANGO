import uuid
from django.db import models
from django.utils import timezone

class TimeStampedModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']

class SystemConfig(models.Model):
    """
    Model lưu trữ các cấu hình động của hệ thống.
    Lý do: Cho phép Admin thay đổi cấu hình nóng (hot-reload) từ UI.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    key = models.CharField(max_length=100, unique=True)
    value = models.JSONField()
    description = models.TextField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'core_system_configs'
        ordering = ['key']

    def __str__(self):
        return self.key

class AuditLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        'identity.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='audit_logs'
    )
    action = models.CharField(max_length=50) # CREATE, UPDATE, DELETE, LOGIN
    module = models.CharField(max_length=100) # e.g. Users, Roles
    record_id = models.CharField(max_length=255, null=True, blank=True)
    payload = models.JSONField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'core_audit_logs'
        ordering = ['-created_at']

class SystemBackup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file_name = models.CharField(max_length=255, help_text="Tên file backup")
    file_path = models.CharField(max_length=500, help_text="Đường dẫn file trên server")
    file_size = models.BigIntegerField(help_text="Kích thước file (bytes)")
    created_by = models.ForeignKey(
        'identity.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='created_backups'
    )
    status = models.CharField(max_length=20, choices=[
        ('PENDING', 'Đang xử lý'),
        ('SUCCESS', 'Thành công'),
        ('FAILED', 'Thất bại')
    ], default='PENDING')
    error_message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'core_system_backups'
        ordering = ['-created_at']

    def __str__(self):
        return self.file_name