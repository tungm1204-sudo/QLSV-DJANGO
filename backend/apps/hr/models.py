"""
Module HR (Quản lý Nhân sự).
Bao gồm thông tin mở rộng của User cho Sinh viên, Giảng viên, Cán bộ.
Tuân thủ rule: Sử dụng UUID, không chứa logic nghiệp vụ trong model.
"""
import uuid
from django.db import models
from apps.identity.models import User
from apps.master_data.models import (
    Department, Major, AdministrativeClass, EducationSystem, PriorityCategory,
    Degree, AcademicTitle, AdmissionType, Ethnicity, Religion, Nationality
)

class Student(models.Model):
    """
    Hồ sơ sinh viên. Liên kết 1-1 với User.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    student_code = models.CharField(max_length=50, unique=True)
    # Thông tin Học tập
    major = models.ForeignKey(Major, on_delete=models.PROTECT, related_name='students', null=True, blank=True)
    administrative_class = models.ForeignKey(AdministrativeClass, on_delete=models.PROTECT, related_name='students', null=True, blank=True)
    education_system = models.ForeignKey(EducationSystem, on_delete=models.PROTECT, related_name='students', null=True, blank=True, help_text="Hệ đào tạo")
    admission_type = models.ForeignKey(AdmissionType, on_delete=models.SET_NULL, null=True, blank=True, related_name='students', help_text="Loại hình tuyển sinh")
    priority_category = models.ForeignKey(PriorityCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='students', help_text="Đối tượng ưu tiên")
    
    status = models.CharField(max_length=50, default='ACTIVE', help_text="ACTIVE, PAUSED, GRADUATED, DROPPED_OUT")
    
    # Thông tin Nhân khẩu học & Liên hệ
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, choices=[('MALE', 'Nam'), ('FEMALE', 'Nữ'), ('OTHER', 'Khác')], null=True, blank=True)
    place_of_birth = models.CharField(max_length=255, null=True, blank=True, help_text="Nơi sinh / Quê quán")
    ethnicity = models.ForeignKey(Ethnicity, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    religion = models.ForeignKey(Religion, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    nationality = models.ForeignKey(Nationality, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    
    personal_email = models.EmailField(null=True, blank=True, help_text="Email cá nhân dự phòng")
    contact_phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True, help_text="Địa chỉ tạm trú hiện tại")
    permanent_address = models.TextField(null=True, blank=True, help_text="Hộ khẩu thường trú")
    
    id_card_number = models.CharField(max_length=50, null=True, blank=True)
    bank_account = models.CharField(max_length=100, null=True, blank=True, help_text="Số TK Ngân hàng - Tên Ngân hàng")
    health_insurance_number = models.CharField(max_length=50, null=True, blank=True, help_text="Mã BHYT")
    parent_info = models.JSONField(null=True, blank=True, help_text="Thông tin phụ huynh: Tên, SĐT, Địa chỉ")
    documents = models.JSONField(null=True, blank=True, help_text="Danh sách URLs giấy tờ đính kèm (CCCD, học bạ)")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hr_students'

    def __str__(self):
        return f"{self.student_code} - {self.user.full_name}"


class Lecturer(models.Model):
    """
    Hồ sơ giảng viên. Liên kết 1-1 với User.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='lecturer_profile')
    lecturer_code = models.CharField(max_length=50, unique=True)
    # Thông tin Công tác
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='lecturers')
    degree = models.ForeignKey(Degree, on_delete=models.SET_NULL, null=True, blank=True, related_name='lecturers')
    academic_title = models.ForeignKey(AcademicTitle, on_delete=models.SET_NULL, null=True, blank=True, related_name='lecturers')
    contract_type = models.CharField(max_length=50, null=True, blank=True, help_text="Cơ hữu, Thỉnh giảng")
    teaching_domain = models.TextField(null=True, blank=True, help_text="Chuyên môn/Lĩnh vực giảng dạy")
    join_date = models.DateField(null=True, blank=True, help_text="Ngày bắt đầu công tác")
    status = models.CharField(max_length=50, default='ACTIVE', help_text="ACTIVE (Đang công tác), RETIRED (Nghỉ hưu), RESIGNED (Nghỉ việc)")
    
    # Thông tin Cá nhân
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, choices=[('MALE', 'Nam'), ('FEMALE', 'Nữ'), ('OTHER', 'Khác')], null=True, blank=True)
    id_card_number = models.CharField(max_length=50, null=True, blank=True)
    place_of_birth = models.CharField(max_length=255, null=True, blank=True)
    ethnicity = models.ForeignKey(Ethnicity, on_delete=models.SET_NULL, null=True, blank=True, related_name='lecturers')
    religion = models.ForeignKey(Religion, on_delete=models.SET_NULL, null=True, blank=True, related_name='lecturers')
    nationality = models.ForeignKey(Nationality, on_delete=models.SET_NULL, null=True, blank=True, related_name='lecturers')
    
    contact_phone = models.CharField(max_length=20, null=True, blank=True)
    personal_email = models.EmailField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    bank_account = models.CharField(max_length=100, null=True, blank=True, help_text="Số TK Ngân hàng - Tên Ngân hàng")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hr_lecturers'

    def __str__(self):
        return f"{self.lecturer_code} - {self.user.full_name}"


class Staff(models.Model):
    """
    Hồ sơ Cán bộ/Nhân viên. Liên kết 1-1 với User.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff_profile')
    staff_code = models.CharField(max_length=50, unique=True)
    # Thông tin Công tác
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='staffs')
    position = models.CharField(max_length=100, null=True, blank=True, help_text="Giáo vụ, Kế toán, Chuyên viên...")
    degree = models.ForeignKey(Degree, on_delete=models.SET_NULL, null=True, blank=True, related_name='staffs')
    responsibilities = models.TextField(null=True, blank=True, help_text="Nhiệm vụ phụ trách")
    join_date = models.DateField(null=True, blank=True, help_text="Ngày bắt đầu công tác")
    status = models.CharField(max_length=50, default='ACTIVE', help_text="ACTIVE, RETIRED, RESIGNED")

    # Thông tin Cá nhân
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, choices=[('MALE', 'Nam'), ('FEMALE', 'Nữ'), ('OTHER', 'Khác')], null=True, blank=True)
    id_card_number = models.CharField(max_length=50, null=True, blank=True)
    contact_phone = models.CharField(max_length=20, null=True, blank=True)
    personal_email = models.EmailField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    bank_account = models.CharField(max_length=100, null=True, blank=True, help_text="Số TK Ngân hàng - Tên Ngân hàng")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hr_staffs'

    def __str__(self):
        return f"{self.staff_code} - {self.user.full_name}"
