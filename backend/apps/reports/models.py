import uuid
from django.db import models
from apps.identity.models import User

# Create your models here.

class CustomReportTemplate(models.Model):
    """
    Lưu cấu hình báo cáo tùy chỉnh của người dùng
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, help_text="Tên mẫu báo cáo")
    description = models.TextField(null=True, blank=True)
    report_type = models.CharField(max_length=50, help_text="STUDENT, FINANCE, ACADEMIC, HR, EXAMS")
    columns = models.JSONField(default=list, help_text="Danh sách các cột cần xuất")
    filters = models.JSONField(default=dict, help_text="Bộ lọc lưu sẵn")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='report_templates')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'reports_custom_templates'
        verbose_name = 'Custom Report Template'
        ordering = ['-created_at']

class DataExportHistory(models.Model):
    """
    Lưu lịch sử xuất dữ liệu (Export)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='export_histories')
    export_type = models.CharField(max_length=100, help_text="Ví dụ: DANH_SACH_SINH_VIEN")
    format = models.CharField(max_length=10, default='EXCEL', choices=[('EXCEL', 'Excel'), ('PDF', 'PDF')])
    filters_applied = models.JSONField(default=dict)
    file_url = models.CharField(max_length=500, null=True, blank=True, help_text="Đường dẫn file đã xuất")
    status = models.CharField(max_length=20, default='COMPLETED', choices=[('PENDING', 'Đang xử lý'), ('COMPLETED', 'Hoàn thành'), ('FAILED', 'Thất bại')])
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'reports_export_histories'
        verbose_name = 'Data Export History'
        ordering = ['-created_at']
