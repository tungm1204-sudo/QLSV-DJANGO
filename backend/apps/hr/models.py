"""
Module HR (Quản lý Nhân sự).
Bao gồm thông tin mở rộng của User cho Sinh viên, Giảng viên, Cán bộ.
Tuân thủ rule: Sử dụng UUID, không chứa logic nghiệp vụ trong model.
"""
import uuid
from django.db import models
from apps.identity.models import User
from apps.master_data.models import Department, Major, AdministrativeClass

class Student(models.Model):
    """
    Hồ sơ sinh viên. Liên kết 1-1 với User.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    student_code = models.CharField(max_length=50, unique=True)
    major = models.ForeignKey(Major, on_delete=models.PROTECT, related_name='students', null=True, blank=True)
    administrative_class = models.ForeignKey(AdministrativeClass, on_delete=models.PROTECT, related_name='students', null=True, blank=True)
    
    status = models.CharField(max_length=50, default='ACTIVE', help_text="ACTIVE, PAUSED, GRADUATED, DROPPED_OUT")
    
    contact_phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    id_card_number = models.CharField(max_length=50, null=True, blank=True)
    parent_info = models.JSONField(null=True, blank=True, help_text="Thông tin phụ huynh: Tên, SĐT, Địa chỉ")
    documents = models.JSONField(null=True, blank=True, help_text="Danh sách URLs giấy tờ đính kèm (CCCD, học bạ)")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'students'

    def __str__(self):
        return f"{self.student_code} - {self.user.full_name}"


class Lecturer(models.Model):
    """
    Hồ sơ giảng viên. Liên kết 1-1 với User.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='lecturer_profile')
    lecturer_code = models.CharField(max_length=50, unique=True)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='lecturers')
    
    academic_title = models.CharField(max_length=100, null=True, blank=True, help_text="Thạc sĩ, Tiến sĩ, PGS, GS...")
    contract_type = models.CharField(max_length=50, null=True, blank=True, help_text="Cơ hữu, Thỉnh giảng")
    teaching_domain = models.TextField(null=True, blank=True, help_text="Chuyên môn/Lĩnh vực giảng dạy")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'lecturers'

    def __str__(self):
        return f"{self.lecturer_code} - {self.user.full_name}"


class Staff(models.Model):
    """
    Hồ sơ Cán bộ/Nhân viên. Liên kết 1-1 với User.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff_profile')
    staff_code = models.CharField(max_length=50, unique=True)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='staffs')
    
    position = models.CharField(max_length=100, null=True, blank=True, help_text="Giáo vụ, Kế toán, Chuyên viên...")
    responsibilities = models.TextField(null=True, blank=True, help_text="Nhiệm vụ phụ trách")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'staffs'

    def __str__(self):
        return f"{self.staff_code} - {self.user.full_name}"
