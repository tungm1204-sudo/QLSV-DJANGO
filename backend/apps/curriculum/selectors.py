"""
Curriculum Selectors
====================
Tầng truy vấn DB đọc (Read-only) cho Module Đào tạo.
Bắt buộc dùng select_related với FK.
"""
from django.db.models import QuerySet
from .models import Course, TrainingProgram, Prerequisite

class CourseSelector:
    @staticmethod
    def get_courses() -> QuerySet[Course]:
        """Lấy danh sách môn học kèm thông tin Ngành học."""
        return Course.objects.select_related('major').all()

class TrainingProgramSelector:
    @staticmethod
    def get_training_programs() -> QuerySet[TrainingProgram]:
        """Lấy danh sách Chương trình đào tạo kèm thông tin Ngành học."""
        return TrainingProgram.objects.select_related('major').all()

class PrerequisiteSelector:
    @staticmethod
    def get_prerequisites() -> QuerySet[Prerequisite]:
        """Lấy danh sách môn tiên quyết kèm thông tin các môn học liên quan."""
        return Prerequisite.objects.select_related('course', 'required_course').all()
