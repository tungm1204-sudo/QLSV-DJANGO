"""
Curriculum Services
===================
Tầng xử lý Business Logic (Create/Update/Delete) cho Module Đào tạo.
Bảo vệ tính toàn vẹn dữ liệu.
"""
from django.db import transaction
from django.core.exceptions import ValidationError
from .models import Course, TrainingProgram, Prerequisite

class CourseService:
    @staticmethod
    @transaction.atomic
    def delete_course(course: Course) -> None:
        """
        Xóa Môn học.
        Why: Bắt buộc kiểm tra ràng buộc logic xem môn này có đang bị dùng làm 
             môn tiên quyết cho môn khác hay không trước khi xóa.
        """
        if course.prerequisites.exists() or course.required_by.exists():
            raise ValidationError("Không thể xóa môn học đang có ràng buộc làm môn tiên quyết.")
        course.delete()

class TrainingProgramService:
    @staticmethod
    @transaction.atomic
    def delete_training_program(program: TrainingProgram) -> None:
        """Xóa Chương trình đào tạo."""
        program.delete()

class PrerequisiteService:
    @staticmethod
    @transaction.atomic
    def delete_prerequisite(prerequisite: Prerequisite) -> None:
        """Xóa điều kiện tiên quyết."""
        prerequisite.delete()
