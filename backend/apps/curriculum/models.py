"""
Curriculum Models
=================
Định nghĩa các Data Model cho Module Quản lý Đào tạo (Khung chương trình, Môn học).
Kế thừa TimeStampedModel để có sẵn id (UUID) và timestamps.
"""
from django.db import models
from apps.core.models import TimeStampedModel
from apps.master_data.models import Major

class Course(TimeStampedModel):
    """
    Model lưu trữ danh mục Môn học.
    - Cần gắn với một Ngành học cụ thể.
    """
    code = models.CharField(max_length=50, unique=True, help_text="Mã môn học (VD: IT101)")
    name = models.CharField(max_length=255, help_text="Tên môn học")
    credits = models.IntegerField(help_text="Số tín chỉ (VD: 3)")
    major = models.ForeignKey(Major, on_delete=models.PROTECT, related_name='courses', help_text="Thuộc ngành học nào")
    is_active = models.BooleanField(default=True, help_text="Trạng thái hoạt động")

    class Meta:
        db_table = 'curriculum_courses'

    def __str__(self) -> str:
        return f"{self.code} - {self.name}"

class TrainingProgram(TimeStampedModel):
    """
    Model Khung chương trình đào tạo.
    - Tương ứng với một Ngành học.
    """
    code = models.CharField(max_length=50, unique=True, help_text="Mã chương trình (VD: CTTT-CNTT)")
    name = models.CharField(max_length=255, help_text="Tên chương trình đào tạo")
    major = models.ForeignKey(Major, on_delete=models.PROTECT, related_name='training_programs', help_text="Chương trình thuộc ngành nào")
    total_credits = models.IntegerField(help_text="Tổng số tín chỉ yêu cầu tốt nghiệp")
    is_active = models.BooleanField(default=True, help_text="Trạng thái hoạt động")

    class Meta:
        db_table = 'curriculum_training_programs'

    def __str__(self) -> str:
        return self.code

class Prerequisite(TimeStampedModel):
    """
    Model lưu trữ điều kiện Môn tiên quyết.
    - Môn học B yêu cầu phải học môn học A trước.
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='prerequisites', help_text="Môn học đang xét")
    required_course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='required_by', help_text="Môn học bắt buộc phải học trước")

    class Meta:
        db_table = 'curriculum_prerequisites'
        unique_together = ('course', 'required_course')

    def __str__(self) -> str:
        return f"{self.course.code} requires {self.required_course.code}"
