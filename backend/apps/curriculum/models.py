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
    course_type = models.ForeignKey('master_data.CourseType', on_delete=models.PROTECT, related_name='courses', null=True, help_text="Loại học phần")
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

class EquivalentCourse(TimeStampedModel):
    """
    Model lưu trữ Học phần thay thế / tương đương.
    - Môn học B có thể thay thế cho Môn học A nếu chương trình đào tạo thay đổi.
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='equivalent_to', help_text="Môn học trong khung chương trình cũ")
    equivalent_course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='equivalent_for', help_text="Môn học mới dùng để thay thế")

    class Meta:
        db_table = 'curriculum_equivalent_courses'
        unique_together = ('course', 'equivalent_course')

    def __str__(self) -> str:
        return f"{self.equivalent_course.code} is equivalent to {self.course.code}"

class TrainingPlan(TimeStampedModel):
    """
    Kế hoạch đào tạo năm học.
    - Cấp vĩ mô, gom nhóm các Lớp học phần dự kiến mở trong một học kỳ.
    """
    STATUS_CHOICES = [
        ('DRAFT', 'Nháp'),
        ('PENDING', 'Chờ duyệt'),
        ('APPROVED', 'Đã duyệt'),
        ('REJECTED', 'Từ chối'),
    ]
    name = models.CharField(max_length=255, help_text="Tên kế hoạch (VD: Kế hoạch HK1 - 2024 Khoa CNTT)")
    semester = models.ForeignKey('master_data.Semester', on_delete=models.PROTECT, related_name='training_plans')
    department = models.ForeignKey('master_data.Department', on_delete=models.PROTECT, related_name='training_plans', help_text="Khoa chủ quản lập kế hoạch")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    created_by = models.ForeignKey('identity.User', on_delete=models.SET_NULL, null=True, related_name='created_plans')
    approved_by = models.ForeignKey('identity.User', on_delete=models.SET_NULL, null=True, related_name='approved_plans')

    class Meta:
        db_table = 'curriculum_training_plans'

    def __str__(self) -> str:
        return self.name

class CourseOffering(TimeStampedModel):
    """
    Lớp học phần.
    - Đại diện cho 1 môn học được mở thực tế trong 1 học kỳ, có giảng viên giảng dạy.
    """
    STATUS_CHOICES = [
        ('PLANNED', 'Theo kế hoạch'),
        ('OPEN', 'Mở đăng ký'),
        ('CLOSED', 'Đóng đăng ký'),
        ('CANCELLED', 'Đã hủy'),
    ]
    training_plan = models.ForeignKey(TrainingPlan, on_delete=models.CASCADE, related_name='course_offerings', help_text="Thuộc Kế hoạch đào tạo nào")
    course = models.ForeignKey(Course, on_delete=models.PROTECT, related_name='offerings')
    semester = models.ForeignKey('master_data.Semester', on_delete=models.PROTECT, related_name='course_offerings')
    lecturer = models.ForeignKey('hr.Lecturer', on_delete=models.SET_NULL, null=True, blank=True, related_name='course_offerings', help_text="Giảng viên phụ trách")
    min_capacity = models.IntegerField(default=10, help_text="Sĩ số tối thiểu")
    max_capacity = models.IntegerField(default=50, help_text="Sĩ số tối đa")
    current_enrollment = models.IntegerField(default=0, help_text="Số lượng sinh viên đã đăng ký")
    registration_deadline = models.DateTimeField(null=True, blank=True)
    
    # Trọng số điểm (đúng chuẩn DBML)
    attendance_weight = models.DecimalField(max_digits=3, decimal_places=2, default=0.10, help_text="Trọng số điểm chuyên cần (0.00 -> 1.00)")
    midterm_weight = models.DecimalField(max_digits=3, decimal_places=2, default=0.20, help_text="Trọng số điểm giữa kỳ")
    final_weight = models.DecimalField(max_digits=3, decimal_places=2, default=0.70, help_text="Trọng số điểm cuối kỳ")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PLANNED')

    class Meta:
        db_table = 'curriculum_course_offerings'

    def __str__(self) -> str:
        return f"{self.course.code} - {self.semester.name}"

class Schedule(TimeStampedModel):
    """
    Thời khóa biểu cho Lớp học phần.
    - Mỗi lớp học phần có thể có nhiều buổi học trong tuần.
    """
    DAY_CHOICES = [
        ('MONDAY', 'Thứ 2'),
        ('TUESDAY', 'Thứ 3'),
        ('WEDNESDAY', 'Thứ 4'),
        ('THURSDAY', 'Thứ 5'),
        ('FRIDAY', 'Thứ 6'),
        ('SATURDAY', 'Thứ 7'),
        ('SUNDAY', 'Chủ nhật'),
    ]
    course_offering = models.ForeignKey(CourseOffering, on_delete=models.CASCADE, related_name='schedules')
    day_of_week = models.CharField(max_length=20, choices=DAY_CHOICES, help_text="Ngày học trong tuần")
    start_period = models.IntegerField(help_text="Tiết bắt đầu (1-12)")
    end_period = models.IntegerField(help_text="Tiết kết thúc (1-12)")
    room = models.CharField(max_length=50, help_text="Mã phòng học (nhập tay hoặc map với danh mục phòng học)")

    class Meta:
        db_table = 'curriculum_schedules'

    def __str__(self) -> str:
        return f"{self.course_offering.course.code} - {self.day_of_week} ({self.start_period}-{self.end_period})"
