"""
Curriculum Models
=================
Định nghĩa các Data Model cho Module Quản lý Đào tạo (Khung chương trình, Môn học).
Kế thừa TimeStampedModel để có sẵn id (UUID) và timestamps.
"""
from django.db import models
from apps.core.models import TimeStampedModel
from apps.master_data.models import Major, Department, Cohort, Specialization

class Course(TimeStampedModel):
    """
    Model lưu trữ danh mục Môn học.
    - Cần gắn với một Ngành học cụ thể.
    """
    code = models.CharField(max_length=50, unique=True, help_text="Mã môn học (VD: IT101)")
    name = models.CharField(max_length=255, help_text="Tên môn học")
    credits = models.IntegerField(help_text="Tổng số tín chỉ (VD: 3)")
    theory_credits = models.IntegerField(default=0, help_text="Số tín chỉ lý thuyết")
    practical_credits = models.IntegerField(default=0, help_text="Số tín chỉ thực hành")
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='courses', help_text="Thuộc Bộ môn/Khoa quản lý")
    course_type = models.ForeignKey('master_data.CourseType', on_delete=models.PROTECT, related_name='courses', null=True, blank=True, help_text="Loại học phần")
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
    specialization = models.ForeignKey(Specialization, on_delete=models.PROTECT, null=True, blank=True, related_name='training_programs', help_text="Chuyên ngành áp dụng (nếu có)")
    cohort = models.ForeignKey(Cohort, on_delete=models.PROTECT, related_name='training_programs', help_text="Áp dụng cho khóa nào")
    total_credits = models.IntegerField(help_text="Tổng số tín chỉ yêu cầu tốt nghiệp")
    is_active = models.BooleanField(default=True, help_text="Trạng thái hoạt động")

    class Meta:
        db_table = 'curriculum_training_programs'

    def __str__(self) -> str:
        return self.code

class KnowledgeBlock(TimeStampedModel):
    """
    Khối kiến thức / Nhóm học phần trong một Chương trình đào tạo.
    """
    training_program = models.ForeignKey(TrainingProgram, on_delete=models.CASCADE, related_name='knowledge_blocks')
    code = models.CharField(max_length=50, help_text="Mã khối (VD: K1-DAICUONG)")
    name = models.CharField(max_length=255, help_text="Tên khối (VD: Khối kiến thức chuyên ngành)")
    
    mandatory_credits = models.PositiveSmallIntegerField(default=0, help_text="Số TC bắt buộc phải đạt")
    elective_credits = models.PositiveSmallIntegerField(default=0, help_text="Số TC tự chọn tối thiểu phải đạt")
    
    order = models.PositiveSmallIntegerField(default=1)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'curriculum_knowledge_blocks'
        constraints = [
            models.UniqueConstraint(
                fields=['training_program', 'code'],
                name='unique_training_program_block_code'
            )
        ]

    def __str__(self) -> str:
        return f"[{self.code}] {self.name}"

class TrainingProgramCourse(TimeStampedModel):
    """
    Chi tiết môn học trong khung chương trình đào tạo.
    """
    training_program = models.ForeignKey(TrainingProgram, on_delete=models.CASCADE, related_name='program_courses')
    knowledge_block = models.ForeignKey(KnowledgeBlock, on_delete=models.CASCADE, related_name='courses')
    course = models.ForeignKey(Course, on_delete=models.PROTECT, related_name='training_program_courses')
    
    semester_expected = models.PositiveSmallIntegerField(help_text="Học kỳ dự kiến (VD: 1-12)")
    is_mandatory = models.BooleanField(default=True, help_text="True: Bắt buộc | False: Tự chọn")
    
    notes = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'curriculum_training_program_courses'
        unique_together = ('training_program', 'course')

    def clean(self):
        from django.core.exceptions import ValidationError
        super().clean()
        
        # Rule 2: Ensure the knowledge_block belongs to the same training_program
        if self.knowledge_block_id and self.training_program_id:
            if self.knowledge_block.training_program_id != self.training_program_id:
                raise ValidationError({
                    'knowledge_block': 'Khối kiến thức này không thuộc Chương trình đào tạo đã chọn.'
                })
                
        # Rule 5: semester_expected must be >= 1
        if self.semester_expected is not None and self.semester_expected < 1:
            raise ValidationError({
                'semester_expected': 'Học kỳ dự kiến phải lớn hơn hoặc bằng 1.'
            })

    def __str__(self) -> str:
        return f"{self.training_program.code} - {self.course.code}"


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
    room = models.ForeignKey('master_data.Room', on_delete=models.PROTECT, related_name='schedules', help_text="Phòng học")

    class Meta:
        db_table = 'curriculum_schedules'

    def __str__(self) -> str:
        return f"{self.course_offering.course.code} - {self.day_of_week} ({self.start_period}-{self.end_period})"
