"""
Curriculum Selectors
====================
Tầng truy vấn DB đọc (Read-only) cho Module Đào tạo.
Bắt buộc dùng select_related với FK.
"""
from django.db.models import QuerySet
from .models import Course, TrainingProgram, Prerequisite, EquivalentCourse, TrainingPlan, CourseOffering, Schedule

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

class EquivalentCourseSelector:
    @staticmethod
    def get_equivalent_courses():
        return EquivalentCourse.objects.select_related('course', 'equivalent_course').all()

class TrainingPlanSelector:
    @staticmethod
    def get_training_plans() -> QuerySet[TrainingPlan]:
        return TrainingPlan.objects.select_related('department', 'created_by', 'approved_by').all()

class CourseOfferingSelector:
    @staticmethod
    def get_course_offerings() -> QuerySet[CourseOffering]:
        return CourseOffering.objects.select_related('training_plan', 'course', 'lecturer').all()

class ScheduleSelector:
    @staticmethod
    def get_schedules() -> QuerySet[Schedule]:
        return Schedule.objects.select_related('course_offering', 'course_offering__course', 'course_offering__lecturer').all()
