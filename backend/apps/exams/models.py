import uuid
from django.db import models
from apps.core.models import TimeStampedModel
from apps.master_data.models import Semester, Room
from apps.curriculum.models import CourseOffering
from apps.hr.models import Student, Staff
from apps.identity.models import User
from apps.enrollment.models import Enrollment

class ExamSession(TimeStampedModel):
    """Kỳ thi (Ví dụ: Kỳ thi cuối kỳ 1 2024-2025)"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='exam_sessions')
    exam_type = models.ForeignKey('master_data.ExamType', on_delete=models.SET_NULL, null=True, related_name='exam_sessions')
    name = models.CharField(max_length=255, help_text="Tên kỳ thi")
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'exams_exam_sessions'
        ordering = ['-start_date']

    def __str__(self):
        return self.name

class ExamRoom(TimeStampedModel):
    """Phòng thi và ca thi cho một lớp học phần"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    exam_session = models.ForeignKey(ExamSession, on_delete=models.CASCADE, related_name='exam_rooms')
    course_offering = models.ForeignKey(CourseOffering, on_delete=models.CASCADE, related_name='exam_rooms')
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, related_name='exam_rooms')
    
    exam_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    supervisor = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, related_name='supervised_exams', help_text="Giám thị")
    capacity = models.IntegerField(help_text="Số lượng sinh viên tối đa trong phòng thi")
    
    class Meta:
        db_table = 'exams_exam_rooms'
        
    def __str__(self):
        return f"{self.course_offering.course.code} - {self.room.code if self.room else 'N/A'}"

class StudentExamRoom(TimeStampedModel):
    """Phân công sinh viên vào phòng thi"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    exam_room = models.ForeignKey(ExamRoom, on_delete=models.CASCADE, related_name='students')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='exam_rooms')
    
    class Meta:
        db_table = 'exams_student_exam_rooms'
        unique_together = ('exam_room', 'student')

class GradeReview(TimeStampedModel):
    """Đơn phúc khảo điểm"""
    class StatusChoices(models.TextChoices):
        PENDING = 'PENDING', 'Chờ xử lý'
        APPROVED = 'APPROVED', 'Đã chấp nhận'
        REJECTED = 'REJECTED', 'Bị từ chối'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='grade_reviews')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grade_reviews')
    reason = models.TextField(help_text="Lý do xin phúc khảo")
    
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.PENDING)
    reviewed_by = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True, related_name='processed_reviews')
    
    old_score = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    new_score = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    
    class Meta:
        db_table = 'exams_grade_reviews'

    def __str__(self):
        return f"Phúc khảo: {self.student.student_code} - {self.enrollment.course_offering.course.code}"

class GradeHistory(TimeStampedModel):
    """Lịch sử thay đổi điểm số (Audit trail cho điểm)"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='grade_histories')
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='changed_grades')
    reason = models.TextField(help_text="Lý do thay đổi điểm", null=True, blank=True)
    
    old_attendance = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    new_attendance = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    
    old_midterm = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    new_midterm = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    
    old_final = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    new_final = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    
    class Meta:
        db_table = 'exams_grade_histories'
        ordering = ['-created_at']

class StudentAcademicRecord(TimeStampedModel):
    """Hồ sơ học thuật: Lưu GPA/CPA từng kỳ của sinh viên"""
    class AcademicStanding(models.TextChoices):
        EXCELLENT = 'EXCELLENT', 'Xuất sắc'
        GOOD = 'GOOD', 'Giỏi'
        FAIR = 'FAIR', 'Khá'
        AVERAGE = 'AVERAGE', 'Trung bình'
        WEAK = 'WEAK', 'Yếu'
        POOR = 'POOR', 'Kém'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='academic_records')
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='academic_records')
    
    # Điểm học kỳ (hệ 10 và hệ 4)
    semester_gpa = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    semester_gpa_4 = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    semester_credits = models.IntegerField(default=0, help_text="Số tín chỉ đạt trong kỳ")
    
    # Điểm tích lũy (hệ 10 và hệ 4)
    cumulative_gpa = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    cumulative_gpa_4 = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    cumulative_credits = models.IntegerField(default=0, help_text="Tổng tín chỉ tích lũy")
    
    academic_standing = models.CharField(max_length=20, choices=AcademicStanding.choices, null=True, blank=True)
    
    class Meta:
        db_table = 'exams_student_academic_records'
        unique_together = ('student', 'semester')
        ordering = ['student', 'semester__start_date']

    def __str__(self):
        return f"{self.student.student_code} - {self.semester.code}"
