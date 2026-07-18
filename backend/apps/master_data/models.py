"""
Master Data Models
==================
Định nghĩa các bảng dữ liệu danh mục gốc (Master Data) dùng chung cho toàn bộ hệ thống.
Bao gồm: Department (Đơn vị), Major (Ngành học), Room (Phòng học), PriorityCategory (Đối tượng ưu tiên), 
ExamType (Hình thức thi), Cohort (Khóa học), Semester (Học kỳ).
Tất cả model đều kế thừa TimeStampedModel để có sẵn id (UUID) và timestamps.
"""
from django.db import models
from apps.core.models import TimeStampedModel

class EducationSystem(TimeStampedModel):
    """
    Model lưu trữ Hệ đào tạo.
    - VD: Chính quy, Liên thông, Vừa làm vừa học.
    """
    code = models.CharField(max_length=50, unique=True, help_text="Mã hệ đào tạo (VD: CQ)")
    name = models.CharField(max_length=255, help_text="Tên hệ đào tạo (VD: Chính quy)")
    is_active = models.BooleanField(default=True, help_text="Trạng thái hoạt động")

    class Meta:
        db_table = 'master_data_education_systems'

    def __str__(self) -> str:
        return self.name

class Department(TimeStampedModel):
    """
    Model lưu trữ danh mục Khoa/Bộ môn/Phòng ban.
    - Dùng chung cho Quản lý nhân sự và Đào tạo.
    - Có tính chất phân cấp (parent/children).
    """
    class TypeChoices(models.TextChoices):
        FACULTY = 'FACULTY', 'Khoa'
        DEPARTMENT = 'DEPARTMENT', 'Bộ môn'
        CENTER = 'CENTER', 'Trung tâm'
        OFFICE = 'OFFICE', 'Phòng ban'

    code = models.CharField(max_length=50, unique=True, help_text="Mã đơn vị (VD: CNTT, GDTC)")
    name = models.CharField(max_length=255, help_text="Tên đơn vị")
    type = models.CharField(max_length=50, choices=TypeChoices.choices, help_text="Loại đơn vị (Khoa/Bộ môn...)")
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children', help_text="Đơn vị cha (VD: Bộ môn thuộc Khoa)")
    manager_id = models.UUIDField(null=True, blank=True, help_text="ID của Trưởng đơn vị (Tham chiếu lỏng đến bảng Nhân sự)")
    is_active = models.BooleanField(default=True, help_text="Trạng thái hoạt động")

    class Meta:
        db_table = 'master_data_departments'

    def __str__(self) -> str:
        return f"{self.code} - {self.name}"

class Major(TimeStampedModel):
    """
    Model lưu trữ danh mục Ngành học.
    - Phân bổ theo Khoa (Department).
    - Là nền tảng để xây dựng Khung chương trình đào tạo.
    """
    code = models.CharField(max_length=50, unique=True, help_text="Mã ngành học (VD: 7480201)")
    name = models.CharField(max_length=255, help_text="Tên ngành học")
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='majors', help_text="Thuộc khoa/đơn vị nào")
    is_active = models.BooleanField(default=True, help_text="Trạng thái hoạt động")

    class Meta:
        db_table = 'master_data_majors'

    def __str__(self) -> str:
        return self.name

class Specialization(TimeStampedModel):
    """
    Model lưu trữ Chuyên ngành trực thuộc Ngành học.
    """
    code = models.CharField(max_length=50, unique=True, help_text="Mã chuyên ngành")
    name = models.CharField(max_length=255, help_text="Tên chuyên ngành")
    major = models.ForeignKey(Major, on_delete=models.PROTECT, related_name='specializations', help_text="Thuộc ngành học nào")
    is_active = models.BooleanField(default=True, help_text="Trạng thái hoạt động")

    class Meta:
        db_table = 'master_data_specializations'

    def __str__(self) -> str:
        return f"{self.name} ({self.major.name})"

class Room(TimeStampedModel):
    """
    Model lưu trữ danh mục Phòng học.
    - Dùng để xếp thời khóa biểu và lịch thi.
    """
    class TypeChoices(models.TextChoices):
        THEORY = 'THEORY', 'Lý thuyết'
        PRACTICE = 'PRACTICE', 'Thực hành'
        HALL = 'HALL', 'Hội trường'

    class StatusChoices(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Đang dùng'
        MAINTENANCE = 'MAINTENANCE', 'Bảo trì'

    code = models.CharField(max_length=50, unique=True, help_text="Mã phòng (VD: A1-201)")
    name = models.CharField(max_length=255, null=True, blank=True, help_text="Tên/Mô tả phòng")
    type = models.CharField(max_length=50, choices=TypeChoices.choices, help_text="Loại phòng (Lý thuyết, Thực hành)")
    capacity = models.IntegerField(help_text="Sức chứa tối đa (số sinh viên)")
    status = models.CharField(max_length=50, choices=StatusChoices.choices, default=StatusChoices.ACTIVE, help_text="Tình trạng phòng")

    class Meta:
        db_table = 'master_data_rooms'

    def __str__(self) -> str:
        return self.code

class PriorityCategory(TimeStampedModel):
    """
    Model lưu trữ danh mục Đối tượng ưu tiên (TB, LS, Dân tộc thiểu số).
    - Ảnh hưởng đến việc miễn giảm học phí.
    """
    code = models.CharField(max_length=50, unique=True, help_text="Mã ưu tiên (VD: DT1)")
    name = models.CharField(max_length=255, help_text="Tên đối tượng ưu tiên")
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, help_text="Phần trăm giảm học phí (%)")
    is_active = models.BooleanField(default=True, help_text="Trạng thái hoạt động")

    class Meta:
        db_table = 'master_data_priority_categories'

    def __str__(self) -> str:
        return self.name

class ExamType(TimeStampedModel):
    """
    Model lưu trữ danh mục Hình thức thi.
    - VD: Tự luận, Trắc nghiệm, Thực hành, Vấn đáp.
    """
    code = models.CharField(max_length=50, unique=True, help_text="Mã hình thức (VD: TU_LUAN)")
    name = models.CharField(max_length=255, help_text="Tên hình thức thi")
    is_active = models.BooleanField(default=True, help_text="Trạng thái hoạt động")

    class Meta:
        db_table = 'master_data_exam_types'

    def __str__(self) -> str:
        return self.name

class Cohort(TimeStampedModel):
    """
    Model lưu trữ Khóa học của sinh viên.
    - VD: K2024, khóa tuyển sinh năm 2024.
    """
    code = models.CharField(max_length=50, unique=True, help_text="Mã khóa học (VD: K2024)")
    name = models.CharField(max_length=255, help_text="Tên khóa học (VD: Khóa 2024-2028)")
    admission_year = models.IntegerField(help_text="Năm tuyển sinh (VD: 2024)")
    is_active = models.BooleanField(default=True, help_text="Trạng thái hoạt động")

    class Meta:
        db_table = 'master_data_cohorts'

    def __str__(self) -> str:
        return self.code

class AcademicYear(TimeStampedModel):
    """
    Model lưu trữ Năm học.
    - VD: Năm học 2024-2025.
    """
    code = models.CharField(max_length=50, unique=True, help_text="Mã năm học (VD: 2024-2025)")
    name = models.CharField(max_length=255, help_text="Tên năm học (VD: Năm học 2024-2025)")
    is_current = models.BooleanField(default=False, help_text="Có phải là năm học hiện tại không?")
    is_active = models.BooleanField(default=True, help_text="Trạng thái hoạt động")

    class Meta:
        db_table = 'master_data_academic_years'

    def __str__(self) -> str:
        return self.name

class Semester(TimeStampedModel):
    """
    Model lưu trữ Học kỳ trong năm học.
    - VD: Học kỳ 1, Năm học 2024-2025.
    - Dùng để tổ chức xếp thời khóa biểu và thu học phí theo kỳ.
    """
    class SeasonChoices(models.TextChoices):
        HK1 = 'HK1', 'Học kỳ 1'
        HK2 = 'HK2', 'Học kỳ 2'
        HE = 'HE', 'Học kỳ Hè'

    code = models.CharField(max_length=50, unique=True, help_text="Mã học kỳ (VD: 2024-HK1)")
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.PROTECT, related_name='semesters', null=True, help_text="Thuộc năm học nào")
    season = models.CharField(max_length=50, choices=SeasonChoices.choices, help_text="Mùa học kỳ (HK1, HK2, Hè)")
    start_date = models.DateField(help_text="Ngày bắt đầu học kỳ")
    end_date = models.DateField(help_text="Ngày kết thúc học kỳ")
    is_current = models.BooleanField(default=False, help_text="Có phải là học kỳ hiện tại không?")

    class Meta:
        db_table = 'master_data_semesters'

    def __str__(self) -> str:
        return self.code


class AdministrativeClass(TimeStampedModel):
    """
    Lớp hành chính cho sinh viên (Ví dụ: K62-CNTT1).
    Phân biệt với lớp học phần (CourseOffering).
    """
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    major = models.ForeignKey(Major, on_delete=models.PROTECT, related_name='administrative_classes')
    cohort = models.ForeignKey(Cohort, on_delete=models.PROTECT, related_name='administrative_classes')
    advisor_id = models.UUIDField(null=True, blank=True, help_text="ID của Giảng viên cố vấn (sẽ map với hr.Lecturer)")
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'master_data_administrative_classes'
        verbose_name_plural = 'Administrative Classes'

    def __str__(self):
        return self.code
