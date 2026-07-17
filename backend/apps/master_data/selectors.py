"""
Master Data Selectors
=====================
Chứa các function thuần túy để truy vấn (Read-only) dữ liệu từ các bảng danh mục (Master Data).
Tuân thủ chuẩn Service Layer: Đưa toàn bộ việc filter, select_related vào đây để tái sử dụng.
"""
from django.db.models import QuerySet
from .models import Department, Major, Room, PriorityCategory, ExamType, Cohort, Semester

class DepartmentSelector:
    @staticmethod
    def get_departments() -> QuerySet[Department]:
        """
        Lấy danh sách Khoa/Bộ môn.
        Why: Dùng select_related('parent') để chống lỗi N+1 khi FE muốn hiển thị tên đơn vị cha.
        """
        return Department.objects.select_related('parent').all()

class MajorSelector:
    @staticmethod
    def get_majors() -> QuerySet[Major]:
        """
        Lấy danh sách Ngành học.
        Why: Dùng select_related('department') để lấy thông tin Khoa trực tiếp cùng 1 query.
        """
        return Major.objects.select_related('department').all()

class RoomSelector:
    @staticmethod
    def get_rooms() -> QuerySet[Room]:
        """Lấy danh sách Phòng học."""
        return Room.objects.all()

class PriorityCategorySelector:
    @staticmethod
    def get_categories() -> QuerySet[PriorityCategory]:
        """Lấy danh sách Đối tượng ưu tiên."""
        return PriorityCategory.objects.all()

class ExamTypeSelector:
    @staticmethod
    def get_exam_types() -> QuerySet[ExamType]:
        """Lấy danh sách Hình thức thi."""
        return ExamType.objects.all()

class CohortSelector:
    @staticmethod
    def get_cohorts() -> QuerySet[Cohort]:
        """Lấy danh sách Khóa học."""
        return Cohort.objects.all()

class SemesterSelector:
    @staticmethod
    def get_semesters() -> QuerySet[Semester]:
        """Lấy danh sách Học kỳ."""
        return Semester.objects.all()

class SpecializationSelector:
    @staticmethod
    def get_specializations():
        return __import__('apps.master_data.models', fromlist=['Specialization']).Specialization.objects.select_related('major').all()

class EducationSystemSelector:
    @staticmethod
    def get_education_systems():
        return __import__('apps.master_data.models', fromlist=['EducationSystem']).EducationSystem.objects.all()

class AcademicYearSelector:
    @staticmethod
    def get_academic_years():
        return __import__('apps.master_data.models', fromlist=['AcademicYear']).AcademicYear.objects.all()
