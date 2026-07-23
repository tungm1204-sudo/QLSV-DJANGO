"""
Enrollment Models
=================
Định nghĩa Data Model cho Module Quản lý Đăng ký học phần.
Lưu trữ thông tin sinh viên đăng ký vào các Lớp học phần (CourseOffering).
"""
import uuid
from django.db import models
from apps.core.models import TimeStampedModel
from apps.hr.models import Student
from apps.curriculum.models import CourseOffering

class Enrollment(TimeStampedModel):
    """
    Model lưu trữ kết quả đăng ký học phần của sinh viên.
    Sẽ mở rộng các trường điểm số ở Module 5.
    """
    class EnrollmentTypeChoices(models.TextChoices):
        NORMAL = 'NORMAL', 'Học lần đầu'
        RETAKE = 'RETAKE', 'Học lại'
        IMPROVEMENT = 'IMPROVEMENT', 'Học cải thiện'
        ADVANCED = 'ADVANCED', 'Học vượt'

    class StatusChoices(models.TextChoices):
        PENDING = 'PENDING', 'Chờ phê duyệt'
        APPROVED = 'APPROVED', 'Đã phê duyệt'
        REJECTED = 'REJECTED', 'Từ chối'

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course_offering = models.ForeignKey(CourseOffering, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_type = models.CharField(max_length=20, choices=EnrollmentTypeChoices.choices, default=EnrollmentTypeChoices.NORMAL)
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.APPROVED)
    
    # Điểm số (Sẽ được xử lý logic ở Module 5)
    attendance_score = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    midterm_score = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    final_score = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    total_score = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    
    is_locked = models.BooleanField(default=False, help_text="Khóa bản ghi, không cho sửa điểm")

    class Meta:
        db_table = 'enrollment_enrollments'
        unique_together = ('student', 'course_offering') # Một SV chỉ đăng ký 1 lớp của 1 môn trong 1 học kỳ.

    def __str__(self) -> str:
        return f"{self.student.student_code} - {self.course_offering.course.code}"
